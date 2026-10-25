# Driving the marketplace in a browser

## Pick a browser

Use the first option available in the session:

1. **The user's own browser through an extension**, such as Claude in Chrome (`mcp__claude-in-chrome__*`). It reuses the user's sign-ins and password manager, and marketplaces treat it as a normal visitor. If the harness is Claude and the user has Chrome but no extension tools, recommend installing Claude in Chrome before falling back.
2. **Another browser MCP already connected**, such as a Safari, Playwright, or built-in browser pane server. Check the session's tool list; do not install one.
3. **The `agent-browser` CLI**, if `command -v agent-browser` finds it. Follow [agent-browser.md](agent-browser.md). Do not install it without asking.
4. **No browser**: produce listings as text for the user to paste.

Say which option you picked and why in one line.

## Sign-in

- Check first whether the user is already signed in (avatar or inbox link in the header).
- Before any sign-in, ask the user how: they sign in themselves, or you use the password manager integration when the harness offers one. Never type a password yourself.
- Refuse non-essential cookies when the banner offers it.

## Working in the page

- Tell the user in the conversation what you are doing on their account before each step, in one short line: which page you open, what you read, what you fill. API calls are invisible in the browser, so name them too ("Reading your active listings through Vinted's API").
- A browser window you drive stays visible to the user; never switch to a headless or hidden browser on their account.
- Prefer the site's own JSON API through `fetch` in the page (it carries the session cookies) over scraping the DOM. Use `GET` only unless the user approved the change.
- Opening an unread conversation marks it read for the user. List conversations; open only the ones already read or the ones the user asked about.
- Leaving a half-filled listing form raises a "Leave site?" dialog that blocks browser automation, and closing the tab can hang on it. Open a new tab rather than navigating away from a form. To release a stuck form tab once the user agrees to discard it, run in the page `Object.defineProperty(BeforeUnloadEvent.prototype, 'returnValue', {configurable: true, set() {}, get() { return '' }}); BeforeUnloadEvent.prototype.preventDefault = function () {}`, then navigate away and close the tab.
