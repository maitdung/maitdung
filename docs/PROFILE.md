# Maintaining this GitHub profile

The profile is rendered from the repository's root `README.md`. The legacy `index.html` and `style.css` files do not style the GitHub profile README.

## Edit the profile

Edit the relevant Markdown or HTML section in `README.md`. Keep section links aligned with their headings. The layout places About and Tech stack before GitHub insights and Featured projects.

Technology badges are image links. Check that their names remain readable and that the images load in GitHub's Preview tab.

## Rebuild the animated banner

The source is [scripts/render_banner.py](../scripts/render_banner.py).

The current typography uses macOS's built-in Avenir Next font at `/System/Library/Fonts/Avenir Next.ttc`. Run on macOS, or adapt the font function and font indices before using another operating system.

From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install "Pillow>=10,<13"
.venv/bin/python scripts/render_banner.py
```

The script writes:

- `assets/profile-banner-motion.gif`: the animated banner used by the profile.
- `assets/profile-banner-motion.png`: a static preview of the first frame.

The animation has 72 frames at 1600 × 540 pixels and loops continuously. The GIF stores each frame for 80 ms. A shared palette keeps colors consistent across frames.

Edit the text near the top of the script to change the title and subtitle. The `curve` function defines the ribbon's 3D geometry; the frame loop controls rotation, lighting, and particles.

## Check an update

1. Preview the banner and confirm that text is readable at the profile's displayed width.
2. Open the GIF and watch a full loop for clipping, abrupt jumps, or flashes.
3. Confirm that the README points to the intended asset filename.
4. Check section navigation, project links, and third-party statistics images in GitHub.
5. Commit the generated asset alongside any changes to its source.

## Achievement goals

The goal illustrations in the README are not official unlocked achievements. GitHub awards sidebar achievements based on qualifying activity. Update a goal's status only after the award is visible on the account.

Reference: [GitHub profile achievements](https://docs.github.com/en/account-and-profile/reference/profile-reference#earning-achievements).
