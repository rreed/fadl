## FADL (FurAffinity Down...Loader)

This is a yak shaving exercise within a yak shaving exercise: I wanted to get my FurAffinity gallery out of a site that is notoriously flaky for the sake of backing it up, but I also wanted to reupload them, so I wanted to preserve the filenames and such in the process. FA has no public API, I have over a decade of art, and I wasn't about to spend an hour going through ~300 tabs and clicking download.

So obviously I did what any other normal girl would do and instead spent MORE than an hour dusting off some rusty bs4 skills and writing a gallery scraper for a site that has historically STRONGLY resisted scraping.

It's preserved here because certainly someone else has wondered "why can't I easily export my gallery anyway?" and I believe strongly in a user's right to take their data and go wherever they want with it. :)

## Usage

Set it up with `pip3 install -r requirements.txt`; most people will want to make a virtualenv first, but I'm not your mom.

Run it with `python3 -u username` to scrape the gallery of `username` into the current folder (e.g. if you want to scrape Fender's gallery, https://www.furaffinity.net/gallery/fender/, you'd pass `-u fender`).

By default, this runs unauthenticated, and does not have access to anything Spicy™. If you need the Spicy™ content, you'll have to do a bit of extra stuff: first find some way to generate a Netscape cookies text file, similar to the ones used by youtube-dl and other common libraries (I used the [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/) extension for Firefox), store it somewhere, and run this with `python3 -u username -c /path/to/cookies.txt`. If you generated your cookie file while logged in to FA, you will be able to scrape as an authenticated user, giving you access to the Spicy™ content.

## Copyright

(c) Ammy 2023 I guess.