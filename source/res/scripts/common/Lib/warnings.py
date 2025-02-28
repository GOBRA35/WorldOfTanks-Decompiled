# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/common/Lib/warnings.py
# Compiled at: 2058-02-15 09:10:49
"""Python part of the warnings subsystem."""
import linecache
import sys
import types
__all__ = ['warn',
 'warn_explicit',
 'showwarning',
 'formatwarning',
 'filterwarnings',
 'simplefilter',
 'resetwarnings',
 'catch_warnings']

def warnpy3k(message, category=None, stacklevel=1):
    """Issue a deprecation warning for Python 3.x related changes.
    
    Warnings are omitted unless Python is started with the -3 option.
    """
    if sys.py3kwarning:
        if category is None:
            category = DeprecationWarning
        warn(message, category, stacklevel + 1)
    return


def _show_warning(message, category, filename, lineno, file=None, line=None):
    """Hook to write a warning to a file; replace if you like."""
    if file is None:
        file = sys.stderr
        if file is None:
            return
    try:
        file.write(formatwarning(message, category, filename, lineno, line))
    except (IOError, UnicodeError):
        pass

    return


showwarning = _show_warning

def formatwarning(message, category, filename, lineno, line=None):
    """Function to format a warning the standard way."""
    try:
        unicodetype = unicode
    except NameError:
        unicodetype = ()

    try:
        message = str(message)
    except UnicodeEncodeError:
        pass

    s = '%s: %s: %s\n' % (lineno, category.__name__, message)
    line = linecache.getline(filename, lineno) if line is None else line
    if line:
        line = line.strip()
        if isinstance(s, unicodetype) and isinstance(line, str):
            line = unicode(line, 'latin1')
        s += '  %s\n' % line
    if isinstance(s, unicodetype) and isinstance(filename, str):
        enc = sys.getfilesystemencoding()
        if enc:
            try:
                filename = unicode(filename, enc)
            except UnicodeDecodeError:
                pass

    s = '%s:%s' % (filename, s)
    return s


def filterwarnings(action, message='', category=Warning, module='', lineno=0, append=0):
    """Insert an entry into the list of warnings filters (at the front).
    
    'action' -- one of "error", "ignore", "always", "default", "module",
                or "once"
    'message' -- a regex that the warning message must match
    'category' -- a class that the warning must be a subclass of
    'module' -- a regex that the module name must match
    'lineno' -- an integer line number, 0 matches all warnings
    'append' -- if true, append to the list of filters
    """
    import re
    assert action in ('error', 'ignore', 'always', 'default', 'module', 'once'), 'invalid action: %r' % (action,)
    assert isinstance(message, basestring), 'message must be a string'
    assert isinstance(category, (type, types.ClassType)), 'category must be a class'
    assert issubclass(category, Warning), 'category must be a Warning subclass'
    assert isinstance(module, basestring), 'module must be a string'
    assert isinstance(lineno, (int, long)) and lineno >= 0, 'lineno must be an int >= 0'
    item = (action,
     re.compile(message, re.I),
     category,
     re.compile(module),
     int(lineno))
    if append:
        filters.append(item)
    else:
        filters.insert(0, item)


def simplefilter(action, category=Warning, lineno=0, append=0):
    """Insert a simple entry into the list of warnings filters (at the front).
    
    A simple filter matches all modules and messages.
    'action' -- one of "error", "ignore", "always", "default", "module",
                or "once"
    'category' -- a class that the warning must be a subclass of
    'lineno' -- an integer line number, 0 matches all warnings
    'append' -- if true, append to the list of filters
    """
    assert action in ('error', 'ignore', 'always', 'default', 'module', 'once'), 'invalid action: %r' % (action,)
    assert isinstance(lineno, (int, long)) and lineno >= 0, 'lineno must be an int >= 0'
    item = (action,
     None,
     category,
     None,
     int(lineno))
    if append:
        filters.append(item)
    else:
        filters.insert(0, item)
    return


def resetwarnings():
    """Clear the list of warning filters, so that no filters are active."""
    filters[:] = []


class _OptionError(Exception):
    """Exception used by option processing helpers."""
    pass


def _processoptions(args):
    for arg in args:
        try:
            _setoption(arg)
        except _OptionError as msg:
            print >> sys.stderr, 'Invalid -W option ignored:', msg


def _setoption(arg):
    import re
    parts = arg.split(':')
    if len(parts) > 5:
        raise _OptionError('too many fields (max 5): %r' % (arg,))
    while len(parts) < 5:
        parts.append('')

    action, message, category, module, lineno = [ s.strip() for s in parts ]
    action = _getaction(action)
    message = re.escape(message)
    category = _getcategory(category)
    module = re.escape(module)
    if module:
        module = module + '$'
    if lineno:
        try:
            lineno = int(lineno)
            if lineno < 0:
                raise ValueError
        except (ValueError, OverflowError):
            raise _OptionError('invalid lineno %r' % (lineno,))

    else:
        lineno = 0
    filterwarnings(action, message, category, module, lineno)


def _getaction(action):
    if not action:
        return 'default'
    if action == 'all':
        return 'always'
    for a in ('default', 'always', 'ignore', 'module', 'once', 'error'):
        if a.startswith(action):
            return a

    raise _OptionError('invalid action: %r' % (action,))


def _getcategory(category):
    import re
    if not category:
        return Warning
    else:
        if re.match('^[a-zA-Z0-9_]+$', category):
            try:
                cat = eval(category)
            except NameError:
                raise _OptionError('unknown warning category: %r' % (category,))

        else:
            i = category.rfind('.')
            module = category[:i]
            klass = category[i + 1:]
            try:
                m = __import__(module, None, None, [klass])
            except ImportError:
                raise _OptionError('invalid module name: %r' % (module,))

            try:
                cat = getattr(m, klass)
            except AttributeError:
                raise _OptionError('unknown warning category: %r' % (category,))

        if not issubclass(cat, Warning):
            raise _OptionError('invalid warning category: %r' % (category,))
        return cat


def warn(message, category=None, stacklevel=1):
    """Issue a warning, or maybe ignore it or raise an exception."""
    if isinstance(message, Warning):
        category = message.__class__
    if category is None:
        category = UserWarning
    assert issubclass(category, Warning)
    try:
        caller = sys._getframe(stacklevel)
    except ValueError:
        globals = sys.__dict__
        lineno = 1
    else:
        globals = caller.f_globals
        lineno = caller.f_lineno

    if '__name__' in globals:
        module = globals['__name__']
    else:
        module = '<string>'
    filename = globals.get('__file__')
    if filename:
        fnl = filename.lower()
        if fnl.endswith(('.pyc', '.pyo')):
            filename = filename[:-1]
    else:
        if module == '__main__':
            try:
                filename = sys.argv[0]
            except AttributeError:
                filename = '__main__'

        if not filename:
            filename = module
    registry = globals.setdefault('__warningregistry__', {})
    warn_explicit(message, category, filename, lineno, module, registry, globals)
    return


def warn_explicit(message, category, filename, lineno, module=None, registry=None, module_globals=None):
    lineno = int(lineno)
    if module is None:
        module = filename or '<unknown>'
        if module[-3:].lower() == '.py':
            module = module[:-3]
    if registry is None:
        registry = {}
    if isinstance(message, Warning):
        text = str(message)
        category = message.__class__
    else:
        text = message
        message = category(message)
    key = (text, category, lineno)
    if registry.get(key):
        return
    else:
        for item in filters:
            action, msg, cat, mod, ln = item
            if (msg is None or msg.match(text)) and issubclass(category, cat) and (mod is None or mod.match(module)) and (ln == 0 or lineno == ln):
                break
        else:
            action = defaultaction

        if action == 'ignore':
            registry[key] = 1
            return
        linecache.getlines(filename, module_globals)
        if action == 'error':
            raise message
        if action == 'once':
            registry[key] = 1
            oncekey = (text, category)
            if onceregistry.get(oncekey):
                return
            onceregistry[oncekey] = 1
        elif action == 'always':
            pass
        elif action == 'module':
            registry[key] = 1
            altkey = (text, category, 0)
            if registry.get(altkey):
                return
            registry[altkey] = 1
        elif action == 'default':
            registry[key] = 1
        else:
            raise RuntimeError('Unrecognized action (%r) in warnings.filters:\n %s' % (action, item))
        showwarning(message, category, filename, lineno)
        return


class WarningMessage(object):
    """Holds the result of a single showwarning() call."""
    _WARNING_DETAILS = ('message', 'category', 'filename', 'lineno', 'file', 'line')

    def __init__(self, message, category, filename, lineno, file=None, line=None):
        self.message = message
        self.category = category
        self.filename = filename
        self.lineno = lineno
        self.file = file
        self.line = line
        self._category_name = category.__name__ if category else None
        return

    def __str__(self):
        return '{message : %r, category : %r, filename : %r, lineno : %s, line : %r}' % (self.message,
         self._category_name,
         self.filename,
         self.lineno,
         self.line)


class catch_warnings(object):
    """A context manager that copies and restores the warnings filter upon
    exiting the context.
    
    The 'record' argument specifies whether warnings should be captured by a
    custom implementation of warnings.showwarning() and be appended to a list
    returned by the context manager. Otherwise None is returned by the context
    manager. The objects appended to the list are arguments whose attributes
    mirror the arguments to showwarning().
    
    The 'module' argument is to specify an alternative module to the module
    named 'warnings' and imported under that name. This argument is only useful
    when testing the warnings module itself.
    
    """

    def __init__(self, record=False, module=None):
        """Specify whether to record warnings and if an alternative module
        should be used other than sys.modules['warnings'].
        
        For compatibility with Python 3.0, please consider all arguments to be
        keyword-only.
        
        """
        self._record = record
        self._module = sys.modules['warnings'] if module is None else module
        self._entered = False
        return

    def __repr__(self):
        args = []
        if self._record:
            args.append('record=True')
        if self._module is not sys.modules['warnings']:
            args.append('module=%r' % self._module)
        name = type(self).__name__
        return '%s(%s)' % (name, ', '.join(args))

    def __enter__(self):
        if self._entered:
            raise RuntimeError('Cannot enter %r twice' % self)
        self._entered = True
        self._filters = self._module.filters
        self._module.filters = self._filters[:]
        self._showwarning = self._module.showwarning
        if self._record:
            log = []

            def showwarning(*args, **kwargs):
                log.append(WarningMessage(*args, **kwargs))

            self._module.showwarning = showwarning
            return log
        else:
            return None
            return None

    def __exit__(self, *exc_info):
        if not self._entered:
            raise RuntimeError('Cannot exit %r without entering first' % self)
        self._module.filters = self._filters
        self._module.showwarning = self._showwarning


_warnings_defaults = False
try:
    from _warnings import filters, default_action, once_registry, warn, warn_explicit
    defaultaction = default_action
    onceregistry = once_registry
    _warnings_defaults = True
except ImportError:
    filters = []
    defaultaction = 'default'
    onceregistry = {}

_processoptions(sys.warnoptions)
if not _warnings_defaults:
    silence = [ImportWarning, PendingDeprecationWarning]
    if not sys.py3kwarning and not sys.flags.division_warning:
        silence.append(DeprecationWarning)
    for cls in silence:
        simplefilter('ignore', category=cls)

    bytes_warning = sys.flags.bytes_warning
    if bytes_warning > 1:
        bytes_action = 'error'
    elif bytes_warning:
        bytes_action = 'default'
    else:
        bytes_action = 'ignore'
    simplefilter(bytes_action, category=BytesWarning, append=1)
del _warnings_defaults
