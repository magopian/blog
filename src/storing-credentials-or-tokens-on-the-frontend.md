Title: Storing credentials or tokens on the frontend
Date: 2019-11-10 16:17
Category: misc
Tags: security, web


Security is hard.
Also, I'm not a security expert, so please take what you read here with a grain of salt, and let me know if there's anything wrong.

That being out of the way: I went down a rabbit hole lately, when someone told me: "we worked hard to store the auth token in cookies for our frontend, because we previously stored it in localStorage, and it's very insecure".

Indeed a search for ["localStorage insecure"](https://www.google.com/search?q=localstorage+insecure) will return many results.

But then, is storing sensitive data in cookies, like we did in the old days, more secure?

Say you're developing a frontend for some API, or an SPA, and you need to authenticate a user.
Let's break things down, and try to understand what are the risks, what are the tools at our disposal as web developers, and what are some of the solutions.


## Attacks and vulnerabilities

There are two main ways to attack a website:

### CSRF

A [Cross Site Request Forgery](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)) is a very easy attack that works against cookies: a browser willingly attaches cookies to a request that goes to the associated website.

Say I have a cookie created by `https://my.bank.com` with my credentials.
If I end up being tricked to follow a link to `http://bad.com/evil_csrf_fake_form` that displays a form looking like the following:

```html
<form action="https://my.bank.com/account/transfer">
    <input type="hidden" name="to" value="evil_attacker" />
    <input type="hidden" name="amount" value="123456" />
    <input type="submit" value="Click here for a chance of winning a free gift!" />
</form>
```

The browser will happily attach the cookie from `https://my.bank.com` to the request, from any website or form. The backend, upon receiving the request with the attached valid credentials, will happily transfer the money.

### XSS

A [Cross Site Scripting](https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)) attack is usually a bit more elaborate, as it needs to inject some javascript in the rendered page on the attacked website.
Once it's done though, it's basically game over for the website, as the attacker will have access to everything the legitimate javascript code has. Including in-memory data, localStorage, cookies without `httpOnly`.

An attacker could dump the content of the localStorage using a very generic `JSON.stringify(localStorage)`, or target the website specifically and access in-memory data, or forge a fake login form that would look totally legitimate AND be on the legitimate domain.


## Storage and persistence of sensitive data

Nowadays you can store sensitive data like username/password, bearer token, jwt token... either in:

### Memory

Storing in memory means holding the credentials or token in a variable, a redux state, closures or whatever.

**Good**: this is not vulnerable to CSRF, and an XSS attack will need to be targetted towards your specific way of storing the data.

**Bad**: still vulnerable to a targetted XSS attack, and you're not persisting the credentials or token: if the user opens a new tab or restarts their browser, they'll have to re-authenticate.

### localStorage or sessionStorage

Both are nearly identical, the first one persists accross tabs and browser restarts.

**Good**: readable by javascript, very convenient, not vulnerable to CSRF attacks. They are both readable by javascript

**Bad**: readable in a generic way like `JSON.stringify(localStorage)` which makes it very easy for an attacker in case of an XSS

### Cookies

Cookies can be created as `httpOnly`, which means the content isn't readable by javascript. It can also be `sameSite` to defeat CSRF attacks, but beware that this [isn't supported by all the browsers yet](https://caniuse.com/#feat=same-site-cookie-attribute), and is obviously only available if the frontend is served from the same domain.

**Good**: the cookie is automatically attached to any request sent by your frontend. Not vulnerable to XSS if `httpOnly`. Not vulnerable to CSRF if `sameSite`.

**Bad**: Vulnerable to CSRF if you can't use `sameSite` because not supported by all the browsers you target, or the frontend is not on the same domain or you're using an auth solution like [auth0](https://auth0.com/) or [openID](https://openid.net/) that you don't control.


## The problem

### Frontend and backend on the same domain

You control the backend, and the frontend is on the same domain. You're thus only vulnerable to XSS (but then again, an XSS is game over). To minimize the risks you might prefer staying away from local or session storage. 

- the backend stores and reads the session identifier in an `httpOnly` and `sameSite` cookie, and you can even add some [csrf tokens](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#synchronizer-token-pattern) to the mix
- the frontend doesn't have to concern itself with the credentials

If there is an XSS in your frontend, once you fixed it you can remove the open sessions on the backend. Everybody will need to re-authenticate, and the attacker will have lost all privileges. Also make sure they didn't create an admin user in the meantime!

### No control over the backend

Also applies if the backend is on another domain. In such a case, you can't use `sameSite`, and the backend might not support CSRF tokens (eg if it uses stateless authentication).

Let's take a concrete example (using [hasura](https://hasura.io/) and a JWT token) which happens to be the place where I found out about the [perfect solution](https://blog.hasura.io/best-practices-of-using-jwt-with-graphql/#refresh_token_persistance).

A JWT token is a very sensitive piece of data: as long as it isn't expired it will be accepted. Even if you discovered an XSS on your frontend and fixed it, if the attacker has a victim's JWT token, they'll still be able to use it. There's no easy way to revoke a JWT token (see [token invalidation](https://blog.hasura.io/best-practices-of-using-jwt-with-graphql/#logout_token_invalidation)).

So you need to:

- store the JWT token somewhere safe (not in localStorage, not in a cookie as we can't make it `sameSite` and would thus be vulnerable to CSRF attacks)
- make it expire very quickly (say 15 minutes)

This means that a user will have to re-authenticate every 15 minutes, and every new tab or browser restart. Which is obviously a pain.

So here comes [the refresh token](https://blog.hasura.io/best-practices-of-using-jwt-with-graphql/#silent_refresh) to the rescue!

This refresh token is stored in a `httpOnly` cookie: whenever the in-memory JWT token is about to expire (or has expired), the frontend can make a request to some `/authorize` endpoint that will return the new JWT token. The frontend can then store this new short lived token in memory.

It's safe to have this refresh token in a cookie because:

- it won't be readable by javascript, so not vulnerable to an XSS attack
- if attached to a CSRF request, it'll only refresh the tokens (in memory in the user's browser)


## Conclusion

So, do we have the perfect solution with in-memory short lived sensitive data and a refresh token in an `httpOnly` cookie?
Sure, if you're willing (and able) to set it up. It does mean that the auth backend has to support this flow (I believe it's not the case for [auth0](https://auth0.com/docs/flows/concepts/implicit#spas-and-refresh-tokens) as they recommend using [silent authentication](https://auth0.com/docs/api-auth/tutorials/silent-authentication) which still has the limitations of in-memory: no persistence accross tabs/restarts).
It does add an extra layer of complexity compared to a simple solution like persisting the session in localStorage. And it's not a silver bullet in case of an XSS.

You might consider that if an XSS is game over, then you might as well use localStorage which is way more convenient. But then, it's not because a dedicated thief can break any lock that you leave your door open when you leave the house, right? It's a matter of mitigation and reducing the attack surface.

If you don't have anything of value in your house, you might choose to close the door, and leave the keys under the welcome mat for convenience. How did you like my analogy of using localStorage? ;)

By the way, if the "XSS is basically game over" sounds scary, know that there are ways to mitigate those, see an interesting article [Github CSP journey](https://github.blog/2016-04-12-githubs-csp-journey/), and [a challenge](https://github.com/cure53/XSSChallengeWiki/wiki/H5SC-Minichallenge-3:-%22Sh*t,-it%27s-CSP!%22) to learn a bit more about this subject.
