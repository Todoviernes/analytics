# Analytics

Simple analytics system

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy analytics

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd analytics
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd analytics
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd analytics
celery -A config.celery_app worker -B -l info
```

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [Mailpit](https://github.com/axllent/mailpit) with a web interface is available as docker container.

Container mailpit will start automatically when you will run all docker containers.
Please check [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html) for more details how to start all containers.

With Mailpit running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

### Custom Bootstrap Compilation

The generated CSS is set up with automatic Bootstrap recompilation with variables of your choice.
Bootstrap v5 is installed using npm and customised by tweaking your variables in `static/sass/custom_bootstrap_vars`.

You can find a list of available variables [in the bootstrap source](https://github.com/twbs/bootstrap/blob/v5.1.3/scss/_variables.scss), or get explanations on them in the [Bootstrap docs](https://getbootstrap.com/docs/5.1/customize/sass/).

Bootstrap's javascript as well as its dependencies are concatenated into a single file: `static/js/vendors.js`.

## JS Implementation

traking.js

```js
(function () {
  const API_ENDPOINT = "http://localhost:3000"; // Replace with your Django backend URL

  let sessionId = getCookie("session_id");
  if (!sessionId) {
    sessionId = generateUUID();
    setCookie("session_id", sessionId, 365); // Set for 1 year
    // setCookie('_ur', 'oelooooo', 365); // Set for 1 year
  }

  // Function to track generic events
  window.trackEvent = function (eventType, url = window.location.href) {
    const data = {
      session_id: sessionId,
      event_type: eventType,
      url: url,
      utm_source: getParameterByName("utm_source") || "organic",
      utm_medium: getParameterByName("utm_medium") || "",
      user_id: getUserId() || "",
    };
    sendDataToServer(`${API_ENDPOINT}/data_events/capture_event/`, data);
  };

  // Function to track purchases
  window.trackPurchase = function (productId, amount) {
    const data = {
      session_id: sessionId,
      product_id: productId,
      amount: amount,
      utm_source: getParameterByName("utm_source") || "organic",
      utm_medium: getParameterByName("utm_medium") || "",
    };
    sendDataToServer(`${API_ENDPOINT}/data_events/capture_purchase/`, data);
  };

  function sendDataToServer(endpoint, data) {
    fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
      },
      body: new URLSearchParams(data).toString(),
    });
  }

  function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
  }

  function setCookie(name, value, days) {
    let expires = "";
    if (days) {
      let date = new Date();
      date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
      expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
  }

  function generateUUID() {
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(
      /[xy]/g,
      function (c) {
        const r = (Math.random() * 16) | 0,
          v = c === "x" ? r : (r & 0x3) | 0x8;
        return v.toString(16);
      }
    );
  }
  function getUserId() {
    userId = getCookie("_ur");
    return userId;
  }

  function getParameterByName(name, url = window.location.href) {
    name = name.replace(/[\[\]]/g, "\\$&");
    const regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
      results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return "";
    return decodeURIComponent(results[2].replace(/\+/g, " "));
  }
})();
```

### Usage on the External Website

1. Embed the Script:
   Include the `tracking.js` script on every page of your external website where you want to track events or purchases:

```html
<script src="path_to_your_scripts/tracking.js"></script>
```

2. Send Events:
   Wherever you want to track an event or a purchase on the external site, use the respective functions:

```js
// Tracking a page view
trackEvent("page_view");

// Tracking a purchase
trackPurchase("product123", 99.99);
```

Replace `YOUR_DJANGO_DOMAIN` with your actual Django backend domain in the tracking.js. This setup should now allow you to capture both events and purchases on an external site and send the data to your Django analytics system.

## How it works the JS Events

#### trackEvent function

```js
trackEvent("page_view");
```

Here's what this function does:

eventType: Represents the type of event being tracked, like 'page_view', 'button_click', etc. This is a required argument that you provide when calling the function.

url: By default, it captures the current page's URL. This can be helpful to know on which page the event occurred. If you want to manually specify a different URL, you can provide it as a second argument.

The function also captures UTM parameters (utm_source, utm_medium, etc.) from the URL, which are commonly used for campaign tracking. These parameters might look like https://example.com/?utm_source=google&utm_medium=cpc.

### trackPurchase Function

Here's the breakdown:

**productId:** Represents the ID or identifier of the product that was purchased. This is a required argument.

**amount:** Represents the amount or price of the product. This is also a required argument.

Similar to **trackEvent**, this function also captures UTM parameters from the URL

### Getting the required data

1. UTM Parameters: UTM (Urchin Tracking Module) parameters are five variants of URL parameters used by marketers to track the effectiveness of online marketing campaigns. They typically look like this in URLs: ?utm_source=source_name&utm_medium=medium_name.
   The JavaScript function getParameterByName is responsible for extracting these parameters from the current page's URL.

2. Current Page URL: This is captured using window.location.href in JavaScript. It gives the entire URL of the current page.

3. Session ID: This is a unique identifier for a user's session. The function `getCookie("session_id")` tries to fetch an existing session ID from the user's cookies. If it doesn't find one, it generates a new session ID using generateUUID and sets it as a cookie. This helps in tracking a user's journey through multiple events and actions on the site.

## How to Implement

1. Embed the Tracking Script: Firstly, you'll embed the provided tracking.js on every page you want to track.
2. Track Events:

- On a page where you want to track views, you can add the line trackEvent('page_view'); within a `<script>` tag or in your page's JavaScript file.
- For actions like button clicks, you'd use event listeners:

```js
document.getElementById("buyButton").addEventListener("click", function () {
  trackEvent("button_click");
});
```

3. Track Purchases: On pages or scripts that run after a successful purchase, you'd use the `trackPurchase` function with the relevant product ID and amount:

```js
// Example after a successful purchase
trackPurchase("productABC", 120.5);
```

By following these steps, you'll capture user interactions and their journey on your site, from the landing page (potentially with UTM parameters for campaign tracking) to possible actions and purchases.
