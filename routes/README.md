Notes on `routes`
----------------

Here's an explanation for how the `routes` really works in an `express` application.
Everything in `routes` is basically `middleware`, but what exactly is a `middleware`?

> Middleware functions are functions that have access to the request object (req), the response object (res), 
> and the next middleware function in the application’s request-response cycle.

More details can be found on the [express middleware link](https://expressjs.com/en/guide/using-middleware.html).

In `app.js` we have definitions of what kinds of routes to expect i.e. 
- `/`
- `/usuario`
- `/profile`
- `/public`
- `/stats`

If we assume that the routes above are the `base` roots, we have the corresponding `routing functions` which are
executed every time we match a specific route.

> Note: We previously used `app.get()` but now we use `app.use()`. This is because `.use()` allows us
> to define various functions that we can use on the same route based on the action.
>
> `HTTP` supports various `verbs` which are basically instructions to web servers and applications to do
> different tasks, the popular ones are `GET` and `POST` which in the `express` world are mapped to `.get()`
> and `.post()`.

To understand more about `HTTP Methods`, follow this [tutorial.](https://www.w3schools.com/tags/ref_httpmethods.asp)

Now for each `app.use()` function that matches the route we specified, use find the corresponding action in the
corresponding `route\....js`. For example, let us consider `/stats` &rarr; which triggers &rarr; `./routes/stats.js`.

The 
```js
router.get('/', ... {});
```

is the base path of this route i.e. `/stats/` and matches the `GET()` request. If we wanted `/stats/special`, we'd have
a new method in the router only for `/special` making the `./routes/stats` as

```js
router.get('/', ... {});
router.get('/special', ... {});
```

Since the `/special` here is requested to match after `/stats`, the route the user would need to use `/stats/special`.

This method of structuring our code helps us keep each part separate and easier to maintain.