---
title: Contact
meta-title: Contact - Sims Info Hub
meta-description: Contact the Sims Info Hub
author: The Sims Info Hub Team
---

# Contact

<form name="contact" method="POST" netlify>
    <div class="mb-3 form-floating">
        <input
        type="email"
        name="email"
        class="form-control"
        id="emailInput"
        placeholder="name@example.com" />
        <label for="emailInput">Email adress</label>
        <div id="emailHelp" class="form-text">
        We'll never share your email with anyone else.
        </div>
    </div>
    <div class="mb-3 form-floating">
        <textarea
        class="form-control"
        name="message"
        placeholder="Leave a message here"
        id="messageInput"
        style="height: 140px"></textarea>
        <label for="messageInput">Message</label>
    </div>
    <div class="mb-3 form-check">
        <input
        type="checkbox"
        name="privacycheck"
        class="form-check-input"
        id="exampleCheck1" />
        <label class="form-check-label" for="exampleCheck1">
        I have read and accept the
        <a href="/privacypolicy/">Privacy Policy</a>.
        </label>
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
