from string import ascii_letters
from copy import deepcopy
import json
from django.conf import settings

class Matomo(object):
    """
    TODO
    !!!IMPORTANT!!! - Use script piece 1 for configuration commands. NOT IMPLEMENTED

    Allow users to define their own things
    Make the script ordering abide by a rule other than as_received

    The Javascript version of the matomo tracking api

    Context is used to figure out what the user wants from matomo in this instance

    NOTE: These are already in the script

    _paq.push(['trackPageView']);
    
    _paq.push(['enableLinkTracking']);
    
    var u="//%(tracking_url)s/";
    
    _paq.push(['setTrackerUrl', u+'matomo.php']);

    _paq.push(['setSiteId', %(siteid)s]);
    """
    def __init__(self, **kwargs) -> None:
        self.__used_var_names = []
        # Ordering doesn't really matter much here
        self.__onload_scripts = {}
        if not settings.DEBUG:
            site_id = settings.MATOMO_SITE_ID
            tracking_url = settings.MATOMO_TRACKING_URL
        else:
            site_id=1
            tracking_url="ThisIsATest.NoTouchy"
        self.__tracker_configs = {}
        self.__script_ordering = "as_received"
        self.script_end = """
           </script>
           <noscript><p><img src="//%s/piwik.php?idsite=%s" style="border:0;" alt="" /></p></noscript>
            """ % (tracking_url, site_id)
        self.script_start = """
            <script type="text/javascript">
            """
        self.user_script_pieces = {}
        self.script_pieces = {
            # tracking code
            0: \
            """
                var _paq = window._paq || [];
                _paq.push(['trackPageView']);
                _paq.push(['enableLinkTracking']);
                (function() {
                    var u="//%s/";
                    _paq.push(['setTrackerUrl', u+'matomo.php']);
                    _paq.push(['setSiteId', %s]);
            """ % (tracking_url, site_id),
            1: """
                    %s;
                    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
                    g.type='text/javascript'; g.async=true; g.defer=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
                })();
            """,
        }

    def build_script(self):
        """
        TODO Make this respect ordering!!!
        This expects you to have already added all your scripts.
        """
        script = self.script_start
        if len(self.__onload_scripts) > 0:
            script += self.build_onload_script()
        for piece in self.script_pieces.values():
            try:
                script += piece
            except KeyError:
                break
        if settings.MATOMO_USE_DEFAULT_BANNER:
            script += self.bind_event("accept-tracking", "rememberConsent")
            script += self.bind_event("reject-tracking", "forgetConsent")
        return script + self.script_end

    def add_cmd(self, method_name, parameters=[], at_index=-1):
        """
        Add a paq command to the script. It's important to use this instead
        of just adding to the script yourself so the ordering is preserved and
        we know everything is where it needs to be.

        Also, this will likely be expanded in the future to handle
        more than just pushing commands
        """
        key = len(
                    list(self.script_pieces.keys())
                )
        if at_index != -1:
            raise NotImplementedError("\n\nError: Matomo.add_cmd() -> Inserting at a specific index is not yet supported!\n\n")
        self.script_pieces[key] = self.build_paq_cmd(method_name, parameters)

    def add_script_piece(self, script, onload=False):
        """
        Add things that aren't meant to be paq commands.

        Such as the return of Matomo.bind_event()
        """
        key = len(
                    list(self.script_pieces.keys())
                )
        if onload:
            self.__onload_scripts[len(self.__onload_scripts.keys())] = script
            return
        self.script_pieces[key] = script
    
    def build_paq_cmd(self, cmd, args=[]):
        """
        :Args:
            - cmd: The command to be pushed to paq (i.e enableHeartbeatTimer or contentInteraction)
            - args: Arguments to be added to the paq command. This is mainly
                used when building commands to be used on manual event trigger.
            
        :Returns:
            \"_paq.push(['<API Method Name>', 'parameters', 'go', 'here']);\"
        """
        def __to_js_arg(arg):
            """
            Turn 'arg' into its javascript equivalent

            :Args:
                - arg: the argument that's to be converted to its JS equivalent

            :Returns:
                - The javascript counter-part to the argument that was passed
            """
            if isinstance(arg, dict):
                arg_cpy = deepcopy(arg)
                for k, v in arg_cpy.items():
                    arg.pop(k)
                    try:
                        arg[__to_js_arg(k)] = __to_js_arg(v)
                    except Exception as e:
                        raise Exception(f"\n\nMatomoException: ERROR: {e}")
                return arg
            elif isinstance(arg, bool):
                if arg:
                    arg = "true"
                else:
                    arg = "false"
            elif isinstance(arg, list):
                for elem_idx in range(len(arg)):
                    arg[elem_idx] = __to_js_arg(arg[elem_idx])
            return arg

        # Build _paq command
        paq = """
        _paq.push(['%s'""" % (cmd)
        if len(args) > 0:
            paq += ", "
            for arg_idx in range(len(args)):
            # Convert the current argument to javascript equivalent
                current_arg = __to_js_arg(args[arg_idx])
            # If this is anything but a string we don't want quotes...unless we do...Figure out how to do that
                no_quotes = type(current_arg) in [bool, int, dict, list]
                if no_quotes:
                    segment = "%s" % (current_arg)
                else:
                    segment = "'%s'" % (current_arg)
            # We're at the last thing we have to add
                if arg_idx == len(args)-1:
                    segment+="]);"
                else:
                    segment += ", "
            # Add it
                paq += segment
        else:
            paq += "]);"
        return paq

    def bind_event(
        self,
        elem_id, matomo_event=None,
        matomo_args=None, callback=None,
        args=None, js_event="click"
        ):
        """
        Build a javascript command to bind an event to some
        element with a provided callback or generated paq command

        NOTE: You can pass an entire function body to this and it will work.

        :Args:
            - elem_id: Value of the 'class' attribute of the tag
                the event is to be bound to.
            - matomo_event: The matomo event to be pushed to _paq
                such as trackEvent
            - matomo_args: The arguments to be passed with the matomo event
                meaning (using trackEvent) ['Category', 'Action', ...]

        :Return:
            A string of javascript that loops the elements found by 
                document.getElementById and binds the motomo event
                to each element that was found
        """
        var_name = self.__generate_var_name()
        script = """
        let %s = document.getElementById('%s');
        %s.addEventListener('%s',
                    function(){
                        %s;
                    }
                );
        """ 
        if matomo_event and matomo_args:
            if matomo_args:
                return script % (
                    var_name,
                    elem_id,
                    var_name,
                    js_event,
                    self.build_paq_cmd(matomo_event, matomo_args),
                )
            return script % (
                    var_name,
                    elem_id,
                    var_name,
                    js_event,
                    self.build_paq_cmd(matomo_event)
                )
        elif callback:
            if args:
                return script % (
                    var_name,
                    elem_id,
                    var_name,
                    js_event,
                    callback, args,

                )
            return script % (
                    var_name,
                    elem_id,
                    var_name,
                    js_event,
                    callback
                )
        raise Exception("\n\nYou must provide a matomo event with or without args OR your own callback with or without args")

    def __generate_var_name(self):
        """
        Generate a unique variable name
        """
        var_name = ""
        for letter_idx in range(len(ascii_letters)):
            var_name+=ascii_letters[letter_idx]
            if var_name not in self.__used_var_names:
                self.__used_var_names.append(var_name)
                return var_name
            else:
                try:
                    var_name += ascii_letters[letter_idx+1]
                except IndexError:
                    var_name += ascii_letters[0]
        if var_name not in self.__used_var_names:
            self.__used_var_names.append(var_name)
            return var_name
        raise Exception("Matomo Failed to generate variable name!")

    def build_onload_script(self):
        script = """
        window.addEventListener('load', function() {
            """
        if len(self.__onload_scripts) > 0:
            for load_script in self.__onload_scripts.values():
                script += load_script
            return script + "})"
        else:
            return ""

    def can_track(self, request):
        """
        Return True if the user has agreed to be tracked.
        False otherwise
        """
        if request.COOKIES.get('mtm_consent', None):
            return True
        return settings.MATOMO_DEFAULT_CONSENT

