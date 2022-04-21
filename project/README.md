# MY VIRTUAL CLOSET
#### Video Demo:  https://youtu.be/Lb3un3C1mQE
#### Description:

"My virtual closet" is a web application that helps you choose outfits every day and get inspired by other users' outifts.

In application.py, after importing necessary files and functions, I configured Flask and chose upload folder for pictures
of clothes. Next, we configure session and our SQLite database, "closet.db". Then we have lists: TYPES, WEATHER and EVENTS,
where we set up lists of values available fos users to choose.

Then index.html is configured: we take logged in user's clothes from our database and pass them to index.html, where they
are displayed in a bootstrap carousel, so that user can look through them easily.

In choose.html, we want to enable user to choose their outfit. First, we request that user chooses either a top and bottom
outfit or a dress. They may also filter their clothes by weather and event, but that can be omitted. Using those filters
we take tops and dresses from the database and redirect user to appropiate template.

If the user chose tops and bottoms, they are redirected to tops.html, where they can choose a top for their outfit based on
the selected filters. Once they choose, they get bottoms.html and then shoes.html. After choosing shoes, they can confirm
their outfit and they are redirected to myoutfits.html, where we have two carousels: one for top and bottom outfits and the
other for dresses. Outfits are displayed from newest to oldest, so that user can see them chronologically.

Accordingly, if the user chose dresses as their preferred outfit for a given time, they are directed to dresses.html and then
shoes.html. Then they can confirm their outfit and see it in myoutfits.html.

Another feature of the application is Get inspired tab (gallery.html), where user can see outfits (in two carousels again)
that other users created and get inspiration for their own outfits.

To be able to use the virtual closet, you need to upload some clothes to choose from. In Add to closet tab (upload.html),
you can upload pictures of your clothes and use them in your outfits later. User only needs to upload a picture and choose
the type of item (top, bottom, dresss or shoes). They can choose also the weather the item is appropriate for and event, but
they are not necessary. If the user doesn't choose any option, "all" will be saved by default.

Only logged-in users can use their closet, so application also lets users to log in (login.html) or register (register.html).
Once logged in, user can also change their password (change.html) and log out.

In helpers.py, we have 2 functions (taken from pset9, Finance), handling the displaying of errors to user (along with apology.html)
and decorating routes to require login.

In templates layout.html and layout2.html, we set the base of our html templates and link stylesheets. They are identical except
for body background image.
