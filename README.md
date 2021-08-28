# The Class Based Matomo API
# TODO
1. Allow configuration of the tracker before implanting the script
2. Allow args from template to customize the script based on some condition
3. Ignore internal urls only if MATOMO_IGNORE_LOCAL_IPS = True (require MATOMO_LOCAL_IPS = [...] setting)
3. Allow 
# Index
1. [Quick Start](#quick-start)
2. [Setup](#setup)
    1. [Settings](#settings)
    2. [Urls](#urls)
    3. [Templates](#templates)
    4. [Javascript](#javascript)
3. [Using The Views](#views)
    1. [Auto Fired Views](#auto-fired-views)
    2. [Dashboard](#matomo-dashboard-in-django)
4. [API Endpoints](#endpoints)
5. [Advanced Usage](#advanced-usage)

## NOTE
**This does not find auto created models**, it *shouldn't* matter but, if you try to track something and give the endpoint the name of an auto created model, you **WILL** get an error

While working on a website for a client, I realized Matomo wouldn't be able to record exactly what I need without a lot of work and possibly even modifying the source code of Matomo which, I'm not going to risk.

### Quick Start
1. Add "matomo" to your `INSTALLED_APPS` and any settings you'd like ([Shown Here](possible-settings)) in `settings.py`.
2. Add `path("matomo/", include('matomo.urls'))` in your project level `urls.py` file (found in the same directory as settings.py).
3. Inside of any templates you'd like to track or your base template to track wherever you use that template (**NOTE** It is **HIGHLY RECOMMENDED** to do this in your base template instead to allow consistent analytics), simply place "{% matomo %}" in the head tag or wherever you'd like.
Voila! You are now using Matomo Analytics!

How's that for a quick start? (^_^ )

### Setup
After installing, you need to add `matomo` to your `INSTALLED_APPS` setting in `settings.py`.
Then, if you would like to enable tracking for the front end as well, you can add `matomo.context_providers.JsProvider` to your `CONTEXT_PROVIDERS` setting in settings.py.
Adding that to your context processors will use different information in combination to produce a full length Javascript Tracking script complete with all of your settings, enabled features, etc. as well as allowing you to pass arguments to the template tag in case you need to record something conditionally.

**ADD NOTE ABOUT HOW TO CONFIGURE THE PACKAGE TO EFFECT THE GENERATED JAVASCRIPT**

One advantage to using this package is that, if the user rejects tracking, the package will see that and completely remove any matomo scripts from the templates to give 100% peace of mind to both you and your users.

#### Settings
##### Required
MATOMO_SITE_ID - The Site Id you need to use with Matomo
MATOMO_TRACKING_URL - The tracking url you need to use with Matomo

##### General
MATOMO_CONSENT_REQUEST_MSG - A string that will be shown to the user when they are prompted to allow tracking.
[ **Example** ]
MATOMO_CONSENT_REQUEST_MSG = "Please accept our %s, %s and %s to help improve our website!"
###### **WARNING FOR MATOMO_CONSENT_REQUEST_MSG**
**DO NOT** hardcode the variables in consent disclaimers, nor use string formatting for this setting because that needs to happen just prior to being sent to the template and it can't be formatted if there are no empty spaces to format
**NOTE: YOU MUST** use the %s to hold spaces for your disclaimers.

###### Optional
MATOMO_ASK_CONSENT - If True, this package will attempt to include your tracking consent prompt template in any template the tracking javascript is in. If you set the MATOMO_CONSENT_REQUEST_MSG setting... Hint: See [Customization](#customization)

MATOMO_CONSENT_DISCLAIMERS - A dictionary whose keys are a [name to display in the message*](#template-variables) and values are the urls to their corresponding pages.<br/>
   Example being {
       "Terms of Service": "/policies/terms-of-service/",
       "Privacy Policy": "/privacy/policy/",
       "Community Guidelines": "/guidelines/community/"
       }
    Would render the following message to the consent banner (**Just an example**) "Please accept our Terms of Service, Privacy Policy and Community Guidelines to help improve our website!"

#### Templates
It comes with templates.


#### Javascript


### Use with DRF EndPoints
You have the ability to use the Django implementation as an API.
This can be useful if you need to track something that matomo doesn't normally track. 
Take a look at the [API End Points](#endpoints) docs to learn more about what built in end points you have access to.

### Customization
Time to customize the package!


### Advanced Usage
Sending flags to the Matomo object
You'll need to create a custom context processor which will serve as your communication line to the Matomo object.
Inside of that context processor you can 'turn features on or off'. For any feature you would like to turn on, simply refer to the reference docs and prepend "matomo_" to the option. The Matomo object will notice that and add that method to the script
You're able to do a ridiculous amount of things with this.
##### Customizing the tracker
You can customize the tracker