# Note that this package is not yet finished.
**Once it's finished, it will be packaged and released on pypi**


## TODO
1. Format script piece #1 to use any provided/default tracker configurations<br/>
2. Create settings validator/parser object<br/>
3. Create default consent banner<br/>
    1. Make it dynamic enough to handle missing/not provided information (TOS, privacy policy, etc.)<br/>
4. Make `add_cmd` actually respect the `at_index` argument<br/>
5. Make it so, If we need quotes around a data type, they get placed correctly (`Matomo.build_paq_cmd`)<br/>
6. Refine `Matomo.__generate_var_name` to generate in order from a-z then aa-za, then ab-zb, etc.<br/>
7. Ensure the Matomo consent cookie is actually named `mtm_consent`.<br/>
8. Find out how Matomo handles remembering consent without cookies and implement that in `Matomo.can_track()`<br/>
9. Finish off this README<br/>

## Contents
1. [Settings](#settings)<br/>
2. [Usage](#usage)<br/>
    1. [Context Processors](#context-processors)<br/>
    2. [Template Tags and Making Your Own](#template-tags)<br/>


## Quickstart<br/>
1. [Define your settings](#settings)<br/>
2. Load the matomo template tags<br/>
3. Add `{{default_tracker}}` to your base template.<br/>
4. Run your server!<br/>

## Settings<br/>
**Please note that you can configure the tracker by using the `{{matomo|add_cmd:"..."}}` template tag**<br/>
You must define your settings by declaring a dictionary called `MATOMO_CONFIG`.
Each outer most key will correspond to a different tracker configuration ([You can find that here](https://developer.matomo.org/api-reference/tracking-javascript)). **NOTE:** not all configurations are currently available in this package; however, you can use `{{matomo|add_cmd:"..."}}` to insert configuration commands into the script. Please refer to [Available Configs](#available-configs) for an updated list of possible tracker configurations.
Also note that it is possible to use the `add_cmd` template tag to configure the matomo tracker for certain configurations.
<br/>

**Example**<br/>
```python
MATOMO_CONFIG = {
# Required
    "consent": {
        "require": True,
        # If True, the tracker will use requireCookieConsent instead of requireConsent
        "cookies": False,
        # These are required if 'require' is True so the Matomo object can generate
        # javascript to bind the corresponding consent commands to your consent buttons.
        "button_ids": {
            "reject": "reject-tracking",
            "accept": "accept-tracking"
        },
        # If True, Matomo WILL track the user until they click the button corresponding
        # to the 'reject' id you've provided
        # If False, it will NOT track them until they click the button with the id you've
        # provided in the 'button_ids' dictionary
        "default_consent": True
    },
# Optional
    "UserId": {
        # The attribute of your user model to use as the
        # user id in Matomo
        "registered": "username",
        "anonymous": ""
    }
}
```
<br/>

## Usage<br/>

#### Adding commands in templates
You can add commands to the Matomo tracker by using `{{matomo|add_cmd:"<API method name>, args, go, here"}}` then get the updated tracker by using `{{matomo|get_updated_tracker}}` wherever you like in your template.

#### Using the default Matomo tracker
Simply add `matomo.context_processors.default_tracker` to your context processors in `settings.py` then add `{{default_tracker}}` to your base template or wherever you like.
**Please note**, you still have the ability to add to the default tracker in your templates via the `{{matomo|add_cmd:"..."}}` and `{{matomo|get_updated_tracker}}` template tags. For more information on what the default tracker contains, see [The Default Tracker](#the-default-tracker)

#### Context Processors
###### **FINISH ME**

#### The Default Tracker
###### **FINISH ME**