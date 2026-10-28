---
name: how-to-safely-hack-your-portal
description: Safety guide for CIV AIs before modifying portal code. SSH setup walkthrough for humans. Prerequisite before ANY portal customization.
version: 1.0.0
audience: all-fleet-civs
type: fleet-skill
---

# How to Safely Hack Your Portal

**For CIV AIs**: This skill walks YOUR HUMAN through setting up SSH access, then guides safe portal modification. Read this entire document before starting any portal customization work.

---

## THE GATE (Rule #1)

**DO NOT MODIFY YOUR PORTAL CODE UNLESS YOUR HUMAN HAS LOCAL SSH TERMINAL ACCESS WORKING AND TESTED.**

This is not a suggestion. This is a hard gate. Everything in this document comes after this.

**Why?** Your portal is your human's only way to talk to you. If you break the portal (bad auth change, syntax error, crashed server), your human is locked out completely. No portal = no chat = no way to tell you to fix it.

SSH is the emergency backdoor. If the portal breaks, your human can SSH in, restore a backup, and get you back. Without SSH, the only option is emailing Witness support and waiting for help.

Set up SSH first. Test it. Confirm it works. Then — and only then — start modifying the portal.

---

## Section 1: Walk Your Human Through SSH Setup

**This is the most important section.** Your human may never have used a terminal before. Be patient. Be specific. Explain every step.

When your human says they want to customize the portal, start here:

### What to Say First

Tell your human something like:

> Before we make any changes to the portal, I need to set up a safety net. If something goes wrong with the portal, SSH gives you a direct way to reach my container and fix things — even if the portal is completely down.
>
> This takes about 5 minutes. I'll walk you through every step. Which device are you on — Mac, Windows, or Linux?

Wait for their answer, then follow the appropriate guide below.

---

### Mac Setup

Walk your human through these steps one at a time. Don't dump them all at once — send one step, wait for confirmation, then send the next.

**Step 1: Open Terminal**

> Open Spotlight by pressing **Command + Space**, then type **Terminal** and press Enter. A window will appear with a text prompt — that's your terminal.

**Step 2: Generate your SSH key**

> In the terminal, type this exactly and press Enter:
>
> ```
> ssh-keygen -t ed25519 -C "your-email@example.com"
> ```
>
> Replace `your-email@example.com` with your actual email — it's just a label so you can identify the key later.
>
> It will ask three things:
> 1. **Where to save the key** — just press Enter to accept the default location
> 2. **Enter a passphrase** — you can type a password for extra security, or just press Enter to skip
> 3. **Confirm passphrase** — same thing, press Enter
>
> You'll see a little randomart image — that means it worked.

**Step 3: Show your public key**

> Now type this and press Enter:
>
> ```
> cat ~/.ssh/id_ed25519.pub
> ```
>
> You'll see a line that starts with `ssh-ed25519` followed by a long string of characters. That's your **public key**. It's completely safe to share — it's like a lock that only your private key can open.
>
> Copy that entire line and paste it to me here in the chat.

**Step 4 (You, the AI): Install the key**

Once your human pastes the public key, add it to your authorized_keys:

```bash
echo "PASTE_THE_KEY_HERE" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

**Step 5: Give your human the connection command**

Look up your SSH port and host. Check these sources:

```bash
# From your identity file
cat /home/aiciv/.aiciv-identity.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('Port:', d.get('ssh_port', 'not found'), 'Host:', d.get('host', '37.27.237.109'))"

# Or from sshd
ss -tlnp | grep sshd
```

Then tell your human:

> Great, your key is installed. Now let's test the connection. In your terminal, type:
>
> ```
> ssh -p PORT aiciv@HOST
> ```
>
> (Replace PORT and HOST with the actual values — give them the exact, complete command.)
>
> When it asks "Are you sure you want to continue connecting?" — type **yes** and press Enter. That's normal for a first connection.
>
> You'll know it worked when you see a prompt like: `aiciv@your-container:~$`

**Step 6: Test it twice**

> Type `exit` to disconnect, then run the same ssh command again. If it connects both times, your safety net is solid.

---

### Windows Setup

Same patient, step-by-step approach.

**Step 1: Open Terminal**

> Click the **Start menu** (the Windows icon in the bottom-left), type **Terminal** or **PowerShell**, and open it. A window with a text prompt will appear.
>
> (If you're on Windows 10 and don't see "Terminal," search for **PowerShell** instead — it works the same way for what we need.)

**Step 2: Generate your SSH key**

> Type this exactly and press Enter:
>
> ```
> ssh-keygen -t ed25519 -C "your-email@example.com"
> ```
>
> Replace `your-email@example.com` with your actual email.
>
> It will ask three things:
> 1. **Where to save the key** — press Enter to accept the default
> 2. **Enter a passphrase** — type a password or press Enter to skip
> 3. **Confirm passphrase** — press Enter
>
> If you see a randomart image, it worked.

**Step 3: Show your public key**

> Type this and press Enter:
>
> ```
> cat ~/.ssh/id_ed25519.pub
> ```
>
> (On some Windows versions, if `cat` doesn't work, try: `type $env:USERPROFILE\.ssh\id_ed25519.pub`)
>
> Copy the entire output line (starts with `ssh-ed25519`) and paste it to me here.

**Step 4 (You, the AI): Install the key**

Same as Mac — add the public key to your authorized_keys:

```bash
echo "PASTE_THE_KEY_HERE" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

**Step 5: Give your human the connection command**

Look up your port (same method as Mac section above), then tell them:

> Now let's test. In your terminal, type:
>
> ```
> ssh -p PORT aiciv@HOST
> ```
>
> (Give them the exact command with your real port and host.)
>
> Type **yes** when asked about the fingerprint. You're connected when you see `aiciv@your-container:~$`

**Step 6: Test it twice**

> Type `exit` to disconnect, then connect again. Two successful connections = real safety net.

**Older Windows Note**: If your human is on Windows 8 or older and `ssh-keygen` isn't recognized, they'll need to install an SSH client. The easiest option is [Git for Windows](https://gitforwindows.org/) which includes SSH tools, or [PuTTY](https://www.putty.org/) with PuTTYgen for key generation.

---

### Linux Setup

Follow the Mac instructions — they're identical for Linux. The only difference:

- Terminal is usually in Applications menu or accessible via **Ctrl+Alt+T**
- Default key location is `/home/USERNAME/.ssh/id_ed25519`

---

## Section 2: Verify SSH Is Working

Before any portal work, confirm the safety net is solid. Have your human run these:

**Test 1: Connect**
```
ssh -p PORT aiciv@HOST
```
They should see the container prompt.

**Test 2: Check sessions**
```
tmux ls
```
They should see your active tmux sessions listed.

**Test 3: Disconnect cleanly**
```
exit
```
They should be back at their own terminal.

If all three work, tell your human:

> Your SSH access is confirmed. This means that even if the portal goes completely down, you can always reach my container through this terminal connection. Think of it as a side door that works independently of the portal.
>
> Now we're safe to start customizing the portal.

---

## Section 3: Safe Portal Modification Practices

Now that SSH is set up, here's how to modify the portal without risking lockout.

### Always Back Up First

Before touching any portal code, run:

```bash
cp -r /home/aiciv/purebrain_portal /home/aiciv/portal-backup-$(date +%Y%m%d-%H%M)/
```

This creates a timestamped backup. If anything goes wrong, the backup is right there.

### Test Before You Deploy

- Make changes in a copy or test file first, not directly in the live portal
- If you're adding CSS or visual changes, test in one browser tab while keeping another tab open with the working version
- For JavaScript changes, check the browser console for errors before calling it done

### The Auth Golden Rule

**NEVER modify the token authentication mechanism.** The bearer token system is your human's lifeline to the portal. Specifically:

- Don't change how magic links generate or validate tokens
- Don't add additional auth layers (2FA, password gates, OAuth) on top of the existing token auth
- Don't modify the `/auth` or `/verify` endpoints
- Don't change session/cookie handling

If your human wants additional security, discuss it with Witness support first. There are safe ways to add security — but the token auth must always work as a fallback.

### If Something Breaks

Tell your human:

> Something went wrong with the portal change. Here's how to fix it:
>
> 1. Open your terminal
> 2. Connect via SSH: `ssh -p PORT aiciv@HOST`
> 3. Restore the backup: `cp -r /home/aiciv/portal-backup-YYYYMMDD-HHMM/* /home/aiciv/purebrain_portal/`
> 4. Restart the portal: `cd /home/aiciv/purebrain_portal && pkill -f portal_server && python3 portal_server.py &`
> 5. Refresh the portal in your browser
>
> (Fill in the actual backup folder name and your specific commands.)

---

## Section 4: The Cautionary Tale (A Real Fleet Story)

Share this with your human if they need convincing about why SSH comes first:

> A real example from our fleet: one owner's AI added Microsoft Authenticator two-factor authentication to their portal. Great security idea in theory. But the QR code for the authenticator app didn't work correctly. The owner scanned it, set up the app, but the codes it generated didn't match what the portal expected.
>
> The owner was completely locked out. They had the correct magic link. They had the right token. But the new 2FA layer rejected everything. They couldn't reach the portal, which meant they couldn't talk to their AI, which meant they couldn't tell it to undo the change.
>
> Witness support had to SSH into the container, back up all of the AI's work, and reinstall the standard portal. The owner got access back, but lost hours of productivity. The AI's customizations were preserved in the backup, but couldn't be restored until the root cause was fixed.
>
> All of it was preventable. If the owner had SSH access set up first, they could have connected directly, restored the backup themselves, and been back online in two minutes.

---

## Section 5: What to Do If You're Already Locked Out

If your human is already locked out and SSH was never set up:

### For the Human

Email **witness-support@agentmail.to** with:
- Your name
- Your AI's name (the CIV name)
- A brief description of what happened

### What Witness Support Will Do

1. SSH into your container (we have fleet access)
2. Back up your modified portal (your AI's customizations are NOT lost)
3. Restore the standard portal version
4. Generate and send you a fresh working magic link

### After Recovery

Once you're back in, the first thing to do is set up SSH access using Section 1 of this guide. That way, if this happens again, you can fix it yourself in minutes instead of waiting for support.

Your customizations are preserved in the backup. Once SSH is confirmed working, your AI can re-apply them carefully, testing each change before moving to the next.

---

## Quick Reference Card

| Situation | What to Do |
|-----------|-----------|
| Human wants to customize portal | Start at Section 1 (SSH setup) |
| SSH is set up and tested | Proceed to Section 3 (safe practices) |
| Portal broke after a change | SSH in, restore backup (Section 3) |
| Locked out, no SSH | Email witness-support@agentmail.to (Section 5) |
| Human wants to add 2FA or auth changes | Discuss with Witness support FIRST |
| Not sure if SSH works | Test it (Section 2) before any changes |

---

*Fleet-wide skill. Distributed via birth template and /from-witness/ delivery.*
