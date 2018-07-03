import six
from appconf.base import AppConfMetaClass, AppConfOptions, ImproperlyConfigured


class MetaApp(AppConfMetaClass):

    def __new__(cls, name, bases, attrs):
        super_new = super(AppConfMetaClass, cls).__new__
        parents = [b for b in bases if isinstance(b, AppConfMetaClass)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Create the class.
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})
        attr_meta = attrs.pop('Meta', None)
        if attr_meta:
            meta = attr_meta
        else:
            attr_meta = type('Meta', (object,), {})
            meta = getattr(new_class, 'Meta', None)

        prefix = ''

        new_class.add_to_class('_meta', AppConfOptions(meta, prefix))
        new_class.add_to_class('Meta', attr_meta)

        for parent in parents[::-1]:
            if hasattr(parent, '_meta'):
                new_class._meta.names.update(parent._meta.names)
                new_class._meta.defaults.update(parent._meta.defaults)
                new_class._meta.configured_data.update(
                    parent._meta.configured_data)

        for name in filter(str.isupper, list(attrs.keys())):
            prefixed_name = new_class._meta.prefixed_name(name)
            new_class._meta.names[name] = prefixed_name
            new_class._meta.defaults[prefixed_name] = attrs.pop(name)

        # Add all attributes to the class.
        for name, value in attrs.items():
            new_class.add_to_class(name, value)

        new_class._configure()
        for name, value in six.iteritems(new_class._meta.configured_data):
            prefixed_name = new_class._meta.prefixed_name(name)
            setattr(new_class._meta.holder, prefixed_name, value)
            new_class.add_to_class(name, value)

        # Confirm presence of required settings.
        for name in new_class._meta.required:
            prefixed_name = new_class._meta.prefixed_name(name)
            if not hasattr(new_class._meta.holder, prefixed_name):
                raise ImproperlyConfigured('The required setting %s is'
                                           ' missing.' % prefixed_name)

        return new_class


class NoPrefixAppConf(six.with_metaclass(MetaApp)):
    def prefixed_name(self, name):
        return "%s" % name.upper()

    def __init__(self, **kwargs):
        for name, value in six.iteritems(kwargs):
            setattr(self, name, value)

    def __dir__(self):
        return sorted(set(self._meta.names.keys()))

    # For instance access..
    @property
    def configured_data(self):
        return self._meta.configured_data

    def __getattr__(self, name):
        if self._meta.proxy:
            return getattr(self._meta.holder, name)
        raise AttributeError("%s not found. Use '%s' instead." %
                             (name, self._meta.holder_path))

    def __setattr__(self, name, value):
        if name == name.upper():
            setattr(self._meta.holder,
                    self._meta.prefixed_name(name), value)
        object.__setattr__(self, name, value)

    def configure(self):
        """Hook for doing any extra configuration, returning a dictionary.

        containing the configured data.
        """
        return self.configured_data
