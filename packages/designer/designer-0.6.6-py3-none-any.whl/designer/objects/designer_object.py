import difflib

import designer
from typing import List, Optional, Dict

try:
    from weakref import ref as _wref
except ImportError:
    _wref = lambda x: x

from designer.core.scene import Scene
from designer.core.event import Event, register, unregister
from designer.utilities.vector import Vec2D
from designer.core.internal_image import InternalImage, DesignerSurface
from designer.utilities.rect import Rect
from designer.utilities.util import _anchor_offset, _Blit, _CollisionBox
from designer.utilities.animation import Animation


class DesignerObject:
    """
    DesignerObjects are how images and shapes are positioned and drawn onto the screen.
    They aggregate together information such as where to be drawn, their size, and their color.
    Each type of DesignerObject has its own specific kinds of attributes, but all DesignerObjects
    have certain common attributes.
    """
    FIELDS = (
        "rect", "pos",
        "layer",
        "x", "y", "width", "height",
        "size", "scale", "scale_x", "scale_y",
        "anchor",
        "angle", "flip_x", "flip_y", "visible",
        "parent", "mask",
        "alpha"
    )
    _ID = 0

    def __init__(self, parent=None, **kwargs):
        designer.check_initialized()

        if parent is None:
            parent = designer.GLOBAL_DIRECTOR.current_scene

        for obj in [self, *type(self).mro()]:
            if hasattr(obj, '__annotations__'):
                for key in obj.__annotations__:
                    if key in kwargs:
                        setattr(self, key, kwargs.get(key))

        # Unique ID for this object
        self._id = DesignerObject._ID
        DesignerObject._ID += 1

        #: Internal field about how long this DesignerObject has existed
        self._age: int = 0
        #: Whether or not this DesignerObject will not need to be redrawn for a while
        self._static: bool = False
        self._make_static = False

        # Independent Fields
        self._independent_fields = ('_pos', '_size', '_anchor', '_scale', '_angle', '_flip_x', '_flip_y')
        self._layer: Optional[str] = kwargs.get('layer', None)
        self._blend_flags = 0
        self._alpha = kwargs.get('alpha', 1.0)
        self._visible = kwargs.get('visible', True)
        self._pos = Vec2D(kwargs.get('pos')) if 'pos' in kwargs else Vec2D(kwargs.get('x', 0), kwargs.get('y', 0))
        self._size = Vec2D(kwargs.get('size')) if 'pos' in kwargs else Vec2D(kwargs.get('width', 1), kwargs.get('height', 1))
        self._anchor = kwargs.get('anchor', 'center')
        if 'scale' in kwargs and kwargs['scale'] != None:
            s = kwargs.get('scale')
            self._scale = Vec2D((s, s) if isinstance(s, (int, float)) else s)
        else:
            self._scale = Vec2D(kwargs.get('scale_x', 1.0), kwargs.get('scale_y', 1.0))
        self._angle = kwargs.get('angle', 0)
        self._flip_x = kwargs.get('flip_x', False)
        self._flip_y = kwargs.get('flip_y', False)
        self._active = kwargs.get('active', False)
        # TODO: Finish setting up cropping
        self._crop: Optional[Rect] = None
        self._mask: Optional[Rect] = None

        # Dependent fields
        self._offset = Vec2D(0, 0)
        self._computed_layer = parent.scene._get_layer_position(parent, self._layer)
        #: The actual image after it has been scaled/cropped/rotated/etc.
        self._transform_image: Optional[DesignerSurface] = None
        self._transform_offset = Vec2D(0, 0)

        # Animation stuff
        self._animations: List[Animation] = []
        self._progress: Dict[Animation, float] = {}

        # Internal references to parents
        self._parent = _wref(parent)
        self._scene: Scene = _wref(parent.scene)

        # Add it to the world
        if designer.GLOBAL_DIRECTOR.running:
            self._reactivate()

        self.FIELDS = set(self.FIELDS)

    def __repr__(self):
        activated = "" if self._active else "INACTIVE "
        name = type(self).__name__
        return f"<{activated}{name}()>"

    def _active_status(self):
        return "" if self._visible else "HIDDEN " if self._active else "INACTIVE "

    def check_key(self, item):
        if item not in dir(self):
            suggestions = ", ".join(map(repr, difflib.get_close_matches(repr(item), self.FIELDS)))
            if suggestions:
                raise KeyError(f"Key {item!r} not found. Perhaps you meant one of these? {suggestions}")
            else:
                raise KeyError(
                    f"Key {item!r} not found. I didn't recognize that key, you should check the documentation!")

    def __getitem__(self, item):
        """ Allow this object to be treated like a dictionary. """
        self.check_key(item)
        return getattr(self, item)

    def __setitem__(self, key, value):
        """ Allow this object to be treated like a dictionary. """
        self.FIELDS.add(key)
        self.__setattr__(key, value)

    def _set_static(self):
        """
        Forces this class to be static, indicating that it will not be redrawn
        every frame.
        """
        self._make_static = True
        self._static = True

    def __del__(self):
        if self._static:
            self._scene()._remove_static_blit(self)

    def _expire_static(self):
        """
        Force this class to no longer be static; it will be redrawn for a few
        frames, until it has sufficiently aged. This also triggers the collision
        box to be recomputed.

        :rtype: bool
        :returns: whether it was successful
        """
        # Expire static is part of the private API which must
        # be implemented by Sprites that wish to be static.
        if self._static:
            self._scene()._remove_static_blit(self)
        self._static = False
        self._age = 0
        self._set_collision_box()
        return True

    def _make_blank_surface(self):
        self._transform_image = DesignerSurface((1, 1))
        self._recalculate_offset()
        self._expire_static()

    def _default_redraw_transforms(self, target):
        if self._flip_x or self._flip_y:
            target.flip(self._flip_x, self._flip_y)
        # Scale
        if self._scale != (1.0, 1.0):
            new_size = self._scale * target.size
            new_size = (int(new_size[0]), int(new_size[1]))
            if 0 in new_size:
                self._transform_image = DesignerSurface((1, 1))
                self._recalculate_offset()
                self._expire_static()
                return
            target.scale(new_size)
        # Rotate
        if self._angle != 0:
            angle = self._angle % 360
            # old = Vec2D(target.rect.center)
            target.rotate(angle)
            # new = target.rect.center
            # self._transform_offset = old - new
        # Finish updates
        self._transform_image = target._surf
        self._recalculate_offset()
        self._expire_static()

    def _redraw_internal_image(self):
        pass

    def _recalculate_offset(self):
        """
        Recalculates this designer object's offset based on its position, transform
        offset, anchor, its image, and the image's scaling.
        """

    @property
    def rect(self):
        """
        Returns a :class:`Rect <designer.Rect>` representing the position and size
        of this Designer Object's image. Note that if you change a property of this rect
        that it will not actually update this object's properties:

        >>> my_object = DesignerObject()
        >>> my_object.rect.top = 10

        Does not adjust the y coordinate of `my_object`. Changing the rect will
        adjust the object however

        >>> my_object.rect = designer.utilities.rect.Rect(10, 10, 64, 64)
        """
        return Rect(self._pos, self._size)

    @rect.setter
    def rect(self, *rect):
        if len(rect) == 1:
            r = rect[0]
            self.x, self.y = r.x, r.y
            self.width, self.height = r.w, r.h
        elif len(rect) == 2:
            self.pos = rect[0]
            self.size = rect[1]
        elif len(rect) == 4:
            self.x, self.y, self.width, self.height = rect
        else:
            raise ValueError("Too few arguments for the Rect of the Designer Object. Must have 1, 2, or 4")

    @property
    def pos(self):
        """
        The position of a sprite in 2D coordinates, represented as a
        :class:`Vec2D <spyral.Vec2D>`
        """
        return self._pos

    @pos.setter
    def pos(self, value):
        if value == self._pos:
            return
        self._pos = Vec2D(value)
        self._expire_static()

    @property
    def layer(self):
        """
        String. The name of the layer this sprite belongs to. See
        :ref:`layering <ref.layering>` for more.
        """
        return self._layer

    @layer.setter
    def layer(self, value: str):
        if value == self._layer:
            return
        self._layer = value
        self._computed_layer = self._scene()._get_layer_position(self._parent(), value)
        self._expire_static()

    @property
    def x(self) -> int:
        """
        The x coordinate of the object, which will remain synced with the
        position.
        """
        return self.pos[0]

    @x.setter
    def x(self, v: int):
        self.pos = (v, self.y)

    @property
    def y(self):
        """
        The y coordinate of the object, which will remain synced with the
        position. Number
        """
        return self.pos[1]

    @y.setter
    def y(self, v):
        self.pos = (self.x, v)

    @property
    def anchor(self):
        """
        Defines an :ref:`anchor point <ref.anchors>` where coordinates are relative to
        on the internal_image. String.
        """
        return self._anchor

    @anchor.setter
    def anchor(self, value):
        if value == self._anchor:
            return
        self._anchor = value
        self._recalculate_offset()
        self._expire_static()

    @property
    def width(self):
        """
        The width of the object after all transforms. Number.
        """
        return self._size[0]

    @width.setter
    def width(self, value):
        self.size = (value, self.height)

    @property
    def height(self):
        """
        The height of the image after all transforms. Number.
        """
        return self._size[1]

    @height.setter
    def height(self, value):
        self.size = (self.width, value)

    @property
    def size(self):
        """
        The size of the image after all transforms (:class:`Vec2D <designer.utilities.vector.Vec2D>`).
        """
        return self._size

    @size.setter
    def size(self, value):
        self._size = Vec2D(value)
        self._redraw_internal_image()
        self._expire_static()

    @property
    def scale(self):
        """
        A scale factor for resizing the image. When read, it will always contain
        a :class:`designer.utilities.vector.Vec2D` with an x factor and a y factor, but it can be
        set to a numeric value which wil ensure identical scaling along both
        axes.
        """
        return self._scale

    @scale.setter
    def scale(self, value):
        if isinstance(value, (int, float)):
            value = Vec2D(value, value)
        if self._scale == value:
            return
        self._scale = Vec2D(value)
        self._redraw_internal_image()
        self._expire_static()

    @property
    def scale_x(self):
        """
        The x factor of the scaling that's kept in sync with scale. Number.
        """
        return self._scale[0]

    @scale_x.setter
    def scale_x(self, x):
        self.scale = (x, self._scale[1])

    @property
    def scale_y(self):
        """
        The y factor of the scaling that's kept in sync with scale. Number.
        """
        return self._scale[1]

    @scale_y.setter
    def scale_y(self, y):
        self.scale = (self._scale[0], y)

    @property
    def angle(self):
        """
        An angle to rotate the image by. Rotation is computed after scaling and
        flipping, and keeps the center of the original image aligned with the
        center of the rotated image.
        """
        return self._angle

    @angle.setter
    def angle(self, value):
        if self._angle == value:
            return
        self._angle = value
        self._redraw_internal_image()

    @property
    def flip_x(self):
        """
        A boolean that determines whether the object should be flipped
        horizontally.
        """
        return self._flip_x

    @flip_x.setter
    def flip_x(self, value):
        if self._flip_x == value:
            return
        self._flip_x = value
        self._redraw_internal_image()

    @property
    def flip_y(self):
        """
        A boolean that determines whether the object should be flipped
        vertically.
        """
        return self._flip_y

    @flip_y.setter
    def flip_y(self, value):
        if self._flip_y == value:
            return
        self._flip_y = value
        self._redraw_internal_image()

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        if self._alpha == value:
            return
        self._alpha = value
        self._expire_static()

    @property
    def visible(self):
        """
        A boolean indicating whether this object should be drawn.
        """
        return self._visible

    @visible.setter
    def visible(self, value):
        if self._visible == value:
            return
        self._visible = value
        self._expire_static()

    @property
    def active(self) -> bool:
        """
        A boolean indicating whether the object is *active*, aka it should be drawn and have collisions, animations,
        and other events handled. An object is active when it is first created while the game is running, but inactive
        if it is created before the game is started.
        """
        return self._active

    @active.setter
    def active(self, value):
        if value:
            self.reactivate()
        else:
            self.destroy()

    @property
    def scene(self):
        """
        The top-level scene that this object belongs to. Read-only.
        """
        return self._scene()

    window = scene

    @property
    def parent(self):
        """
        The parent of this object, either a :class:`View <designer.objects.view.View>` or a
        :class:`Scene <designer.core.scene.Scene>`. Read-only.
        """
        return self._parent()

    @property
    def mask(self):
        """
        A :class:`Rect <designer.utilities.rect.Rect>` to use instead of the current object's rect
        for computing collisions. `None` if the object's rect should be used.
        """
        return self._mask

    @mask.setter
    def mask(self, value):
        self._mask = value
        self._set_collision_box()

    def _draw(self):
        """
        Internal method for generating this object's blit, unless it is
        invisible or currently static. If it has aged sufficiently or is being
        forced, it will become static; otherwise, it ages one step.
        """
        if not self.visible:
            return
        if self._transform_image is None:
            return
        if self._static:
            return

        # TODO: Make sure this is sufficient
        self._transform_image.set_alpha(int(self._alpha * 255))

        area = Rect(self._transform_image.get_rect())
        b = _Blit(self._transform_image, self._pos - self._offset,
                  area, self._computed_layer, self._blend_flags, False,
                  self._id)

        if self._make_static or self._age > 4:
            b.static = True
            self._make_static = False
            self._static = True
            self._parent()._static_blit(self, b)
            return
        self._parent()._blit(b)
        self._age += 1

    def _set_collision_box(self):
        """
        Updates this object's collision box.
        """
        if self._transform_image is None:
            return
        if self._mask is None:
            area = Rect(self._transform_image.get_rect())
        else:
            area = self._mask
        c = _CollisionBox(self._pos - self._offset, area)
        warped_box = self._parent()._warp_collision_box(c)
        self._scene()._set_collision_box(self, warped_box.rect)

    def destroy(self):
        """
        When you no longer need an Object, you can call this method to have it
        removed from the Scene. This will not remove the object entirely from
        memory if there are other references to it; if you need to do that,
        remember to ``del`` the reference to it.
        """
        self._active = False
        self._scene()._remove_static_blit(self)
        self._scene()._unregister_object(self)
        self._parent()._remove_child(self)
        designer.GLOBAL_DIRECTOR._untrack_object(self)
        unregister('director.render', self._draw)

    def _reactivate(self):
        """
        Internal method for making an Object active again.
        Not a preferred mechanism, may have undefined behavior.

        TODO: Finish this so that it can actually work if people want this.
        """
        self._active = True
        designer.GLOBAL_DIRECTOR._track_object(self)
        self.parent._add_child(self)
        self._scene()._register_object(self)
        self._age = 0
        self._static = False
        self._scene().register('director.render', self._draw)

    # Animation Methods

    def _evaluate(self, animation, progress):
        """
        Performs a step of the given animation, setting any properties that will
        change as a result of the animation (e.g., x position).
        """
        values = animation.evaluate(self, progress)
        for a_property in animation.properties:
            if a_property in values:
                setattr(self, a_property, values[a_property])

    def _run_animations(self, delta):
        """
        For a given time-step (delta), perform a step of all the animations
        associated with this designer object.
        """
        completed = []
        for animation in self._animations:
            self._progress[animation] += delta
            progress = self._progress[animation]
            if progress > animation.duration:
                self._evaluate(animation, animation.duration)
                if animation.loop is True:
                    self._evaluate(animation, progress - animation.duration)
                    self._progress[animation] = progress - animation.duration
                elif animation.loop:
                    current = progress - animation.duration + animation.loop
                    self._evaluate(animation, current)
                    self._progress[animation] = current
                else:
                    completed.append(animation)
            else:
                self._evaluate(animation, progress)
        # Stop all completed animations
        for animation in completed:
            self.stop_animation(animation)

    def animate(self, animation):
        """
        Animates this object given an animation. Read more about
        :class:`animation <designer.animation>`.

        :param animation: The animation to run.
        :type animation: :class:`Animation <designer.Animation>`
        """
        for a in self._animations:
            repeats = a.properties.intersection(animation.properties)
            if repeats:
                # Loop over all repeats
                raise ValueError(f"Cannot animate on properties {repeats} twice")
        if len(self._animations) == 0:
            designer.core.event.register('director.update',
                                         self._run_animations,
                                         ('delta',))
        self._animations.append(animation)
        self._progress[animation] = 0
        self._evaluate(animation, 0.0)
        e = Event(animation=animation, sprite=self)
        # Loop over all possible properties
        for a_property in animation.properties:
            designer.core.event.handle(f"{self.__class__.__name__}.{a_property}.animation.start", e)
        return self

    def stop_animation(self, animation):
        """
        Stops a given animation currently running on this object.

        :param animation: The animation to stop.
        :type animation: :class:`Animation <spyral.Animation>`
        """
        if animation in self._animations:
            self._animations.remove(animation)
            del self._progress[animation]
            e = Event(animation=animation, sprite=self)
            for a_property in animation.properties:
                designer.core.event.handle(f"{self.__class__.__name__}.{a_property}.animation.end", e)
            if len(self._animations) == 0:
                designer.core.event.unregister('director.update', self._run_animations)

    def stop_all_animations(self):
        """
        Stops all animations currently running on this object.
        """
        for animation in self._animations:
            self.stop_animation(animation)

    def collide_other(self, other):
        """
        Returns whether this object is currently colliding with the other
        object. This collision will be computed correctly regarding the objects
        offsetting and scaling within their views.

        :param other: The other object
        :type other: :class:`DesignerObject <designer.objects.designer_object.DesignerObject>`
        :returns: ``bool`` indicating whether this object is colliding with the
                  other object.
        """
        return self._scene().collide_objects(self, other)

    def collide_other_at(self, other, x, y):
        return self._scene().collide_object_at(self, other, x, y)

    def collide_point(self, point):
        """
        Returns whether this object is currently colliding with the position.
        This uses the appropriate offsetting for the object within its views.

        :param point: The point (relative to the scene dimensions).
        :type point: :class:`Vec2D <designer.utilities.vector.Vec2D>`
        :returns: ``bool`` indicating whether this object is colliding with the
                  position.
        """
        return self._scene().collide_point(self, *point)

    def collide_rect(self, rect):
        """
        Returns whether this object is currently colliding with the rect. This
        uses the appropriate offsetting for the object within its views.

        :param rect: The rect (relative to the scene dimensions).
        :type rect: :class:`Rect <designer.utilities.rect.Rect>`
        :returns: ``bool`` indicating whether this object is colliding with the
                  rect.
        """
        return self._scene().collide_rect(self, rect)
