"""Pass 3 per-page depth: Good for line, page sections, FAQs, 6th slide caption.
Frozen spec: shared/colorworks/website/2026-11-03_web-developer-bot-to-coo-cw_pass3-product-depth.md
Copy is data file section C (2026-11-03_pass3-product-depth-data.md) with the 3:58 PM CT COO calls and
Steven's 3:59 PM CT answers. Sources: E = Etsy listing:line, re-read Nov 3 2026; EX = approved example;
PR = products.py; Steven = "Steven, Nov 3 3:59 PM CT".
Rules: no prices; no vinyl type on window, storefront, store-hours, vehicle, fleet (D1); no wording that we
install, pick up or deliver; no gloss, matte, laminate (D2). Plain hyphens only.
sections: (icon, heading, [sentences]); faqs: (question, answer); cap6: (title, caption) for the slide 6 render."""

PASS3 = {
 'wall-murals': dict(
   good='Good for: walls inside your space.',  # PR uses
   sections=[('ruler', 'Sized to your wall', ['Tell us the width and height of the wall, and the mural is made to those measurements.'])],  # PR:13
   faqs=[('Can you use my own photo or artwork?', 'Yes. Send your photo or artwork with your request.')],  # EX:wall-murals-4; E:4605923351:35
   cap6=('A mural across a cafe wall', 'A mural that runs the full width of a cafe wall, floor to ceiling.')),
 'lobby-logo-decals': dict(
   good=None,  # gate 5:18: all PR uses already in the lead, dropped
   sections=[('pen-tool', 'Logo detail', ['Cut logos are one solid color, so a logo with gradients or a photo is simplified to one color.',  # E:4605923351:13
                                          'Very thin lines may be thickened a little so the decal goes on cleanly.',  # E:4605923351:14
                                          'Want every gradient in your logo kept? Full-color vinyl prints carry them.'])],  # EX:full-color-vinyl-prints-1
   faqs=[('Do you match our brand color?', 'Pick from 11 stocked colors, or ask for a custom color and send us the one you use.'),  # E:4605923351:29
         ('Can one order cover the wall behind the desk and the office doors?', 'Yes. Lobby walls, reception areas and office glass can all be in one request.')],  # PR:16
   cap6=('A logo on an office door', 'A cut-vinyl logo on a glass office door, the hallway visible through the glass.')),
 'wayfinding-decals': dict(
   good=None,  # gate 5:18: all PR uses already in the lead, dropped
   sections=[('signpost', 'No-background lettering', ['Room names, arrows and icons are cut with no background, so the wall shows through and they look painted on.',  # E:4606418620:1
                                                      'Each sign arrives on transfer tape, which holds every letter in its place while it goes on.'])],  # E:4606411955:7
   faqs=[('Can you letter room numbers too?', 'Yes. Send the list of rooms with their names and numbers.')],  # EX:wayfinding-decals-1
   cap6=('Arrows on a stairwell landing', 'Arrow and icon decals on a stairwell landing wall.')),
 'window-graphics': dict(
   good=None,  # gate 5:18: all PR uses already in the lead, dropped
   sections=[('ruler', 'Sizes', ['Pick 8, 12, 16, 24 or 30 inch, measured on the longest side of your logo.',  # E:4605923351:26
                                 'A round or square logo fills that size, and a wide logo keeps the width and runs shorter.']),  # E:4605923351:26
             ('type', 'Extra lines', ['Along with your business name, you can add up to 2 more lines, such as the year you opened, a phone number, a website or a street address.']),  # E:4605923351:9
             ('package', 'In the box', ['Each order ships with the decal on transfer tape, a small squeegee and application instructions.'])],  # E:4605923351:21-23
   faqs=[('Will it work on frosted or textured glass?', 'No. It needs smooth glass, so frosted and textured glass are not a fit.'),  # E:4606259782:17
         ('Can it go on the inside of the window?', 'No. This decal is made for the street side only.'),  # E:4605923351:17
         ("What if my window needs a size you don't list?", 'Put the size in your request and we quote it.')],  # E:4605923351:26
   cap6=('A logo on a shop door at dusk', 'A one-color logo on a shop door at dusk, the lit shop behind it.')),
 'store-hours-decals': dict(
   good=None,  # gate 5:18: all PR uses already in the lead, dropped
   sections=[('layout-template', 'Two layouts', ['The 12 x 12 inch layout holds your business name, an OPEN line and your hours.',  # E:4605937336:22
                                                 'The 24 x 24 inch layout is a larger version with text only.',  # E:4605937336:23
                                                 'You can add 1 more line for your phone number or website.',  # E:4605937336:8
                                                 'Sizes are the outside edge of the whole design, so measure the glass first.']),  # E:4605937336:21
             ('droplets', 'Care', ['Let it set for 48 hours before you wash the glass, then use a soft cloth and keep scrapers off the edges.'])],  # E:4605937336:34
   faqs=[('My hours changed. Can you make a new one?', 'Yes. Send the new hours and we make a fresh decal to replace the old one.'),  # EX:store-hours-decals-4
         ('Which color reads best on clear glass?', 'White is the most common choice for clear glass.')],  # E:4605937336:26
   cap6=('Hours beside the door handle', 'An hours decal at eye level beside the door handle, lines shown as simple bars.')),
 'storefront-lettering': dict(
   good=None,  # gate 5:18: all PR uses already in the lead, dropped
   sections=[('ruler', 'Set sizes', ['Every set has 3 pieces: one door decal and two window panels.',  # E:4605946560:5,23-25
                                     'Small set: a 10 x 12 inch door decal and two 12 x 18 inch panels.',  # E:4605946560:23
                                     'Medium set: a 12 x 14 inch door decal and two 18 x 24 inch panels.',  # E:4605946560:24
                                     'Large set: a 12 x 18 inch door decal and two 24 x 36 inch panels.',  # E:4605946560:25
                                     'Larger windows or extra panels are quoted to fit.'])],  # E:4605946560:26
   faqs=[('What can the lettering say?', 'Your shop name, services, menu items, hours or a short tagline.')],  # EX:storefront-lettering-1..5
   cap6=('A three-pane storefront', 'A matching door decal and two window panels across a three-pane storefront.')),
 'vehicle-lettering': dict(
   good='Good for: logo decals for a car, truck or van.',  # PR use not in lead
   sections=[('ruler', 'Door kit sizes', ['Door kits run about 24 x 13.25 inch or about 30 x 16.5 inch on each door.',  # E:4606347028:9-10
                                          'The company name is the biggest line, and USDOT letters are 2 inch or taller.']),  # E:4606347028:11
             ('list-checks', 'How it goes on', ['Clean the spot with soap and water, then rubbing alcohol, and let it dry.',  # E:4606347028:29
                                                'Squeegee from the middle out, then peel the transfer tape back slowly at a low angle.',  # E:4606347028:31
                                                'Skip the car wash for 48 hours.']),  # E:4606347028:32
             ('car', 'Back window', ['For the back window, a full-color graphic on perforated film shows your design outside while the driver still sees out.'])],  # E:4606398481:1
   faqs=[('Do you letter USDOT and MC numbers?', 'Yes. A door kit carries your USDOT number and can add an MC line.'),  # E:4606347028:1
         ('My truck has a sliding back window. Does that work?', 'Yes. The graphic can be split into 3 panels at the slider seams.')],  # E:4606398481:6
   cap6=('A see-through back window', 'A full-color see-through graphic on the back window of an SUV.')),
 'fleet-decals': dict(
   good='Good for: cars, trucks and vans.',  # PR use not in lead
   sections=[('hash', 'Unit numbers', ['Unit numbers come 4 inch tall, about 6 to 9 inch wide for four digits, or 6 inch tall, about 9 to 13.5 inch wide.',  # E:4606343349:10-11
                                       'Smaller 3 inch numbers suit equipment, toolboxes and carts.',  # E:4606343349:15
                                       'Pick a color that contrasts with the paint so each number stands out.'])],  # E:4606343349:18
   faqs=[('Do you make USDOT number sets on their own?', 'Yes, as a set of 2, one for each side.')],  # E:4606313059:4
   cap6=('Four matching trucks', 'Four white trucks in a row, each with the same logo and a number spot shown as bars.')),
 'banners': dict(
   good='Good for: businesses and events.',  # PR use not in lead
   sections=[('sun', 'Inside or out', ['Hang it inside at a fair, market or school event, or outside on your storefront.'])],  # Steven, Nov 3 3:59 PM CT; EX:banners-1,3,5
   faqs=[('Can a banner go outdoors?', 'Yes. Banners can be used indoors and outdoors.'),  # Steven, Nov 3 3:59 PM CT
         ('Does it come with grommets?', 'Grommets are added on request. Ask for them when you send your request.')],  # Steven, Nov 3 3:59 PM CT
   cap6=('A banner on a field fence', 'A vinyl banner tied to a chain-link fence beside a sports field.')),
 'logo-stickers': dict(
   good='Good for: products, events and giveaways.',  # PR use not in lead
   sections=[('package', 'Sizes and packs', ['Packs come in 5, 25, 50 or 100 stickers.',  # E:4605958764:4
                                             'A 2 inch sticker seals mailers and small boxes, and a 3 inch sticker suits products, cups and laptops.']),  # E:4605958764:15
             ('house', 'Indoor use', ['They are printed in full color and made for indoor use.'])],  # E:4605958764:10-11
   faqs=[('What is the smallest order?', 'A pack of 5.'),  # E:4605958764:4
         ('Can a sticker carry a QR code?', 'Yes. Send the link it should open with your request.')],  # EX:logo-stickers-2; PR:41
   cap6=('Mailers sealed with stickers', 'Kraft mailers and shopping bags sealed with round logo stickers in two sizes.')),
 'die-cut-stickers': dict(
   good=None,  # gate 5:18: all PR uses already in the lead, dropped
   sections=[('image-plus', 'Sending your art', ['Send a PNG, JPG, PDF or SVG file of your art.',  # E:4605955948:7
                                                 'Tell us whether to keep or remove the background; simple backgrounds we take out for you.']),  # E:4605955948:8-9
             ('ruler', 'Sizes', ['A 3 inch sticker fits most laptops and water bottles, and a 4 inch sticker is a statement piece.']),  # E:4605955948:19
             ('droplets', 'Care', ['Stick them on clean, dry, smooth surfaces, and wash bottles and tumblers by hand.'])],  # E:4605955948:22
   faqs=[("Can you make a sticker from my pet's photo?", 'Yes. We cut your pet out of the photo and can add a name.'),  # E:4605964056 title
         ('Are they made for outdoors?', 'No, they are made for indoor use.')],  # E:4605955948:3,13
   cap6=('A laptop and a water bottle', 'A laptop lid and a water bottle with die-cut stickers, one bordered and one cut to edge.')),
 'dance-floor-decals': dict(
   good='Good for: a floor decal with your logo or event name.',  # PR use not in lead
   sections=[('square', 'Floors it works on', ['It is made for indoor floors that are smooth and nonporous, such as hardwood or marble.',  # E:1670569316:24
                                               'Textured or porous floors are not a fit, so check the floor with your venue.',  # E:1670569316:24,26
                                               'Final size depends on the design and how many letters it has.']),  # E:1670569316:18
             ('party-popper', 'After the party', ['The decal is cut from removable vinyl and comes up after the event.',  # E:1670569316:1,5
                                                  'Every wedding order comes with a small squeegee.'])],  # E:1670569316:22
   faqs=[('Can we pick our own colors and font?', 'Yes. Custom sizes, colors, designs and fonts are available by request.'),  # E:1670569316:14
         ('Does it come with a background color?', 'No. It is vinyl only, unless you ask for a colored background.')],  # E:1670569316:20
   cap6=('A wreath on hardwood', 'Close up of a cut-vinyl wreath lying flat on hardwood floorboards.')),
 'wedding-monograms': dict(
   good='Good for: welcome decals.',  # PR use not in lead
   sections=[('heart', 'On mirrors and glass', ['Mirrors and glass are smooth enough for it.',  # E:1670569316:24
                                                'Wipe the mirror with rubbing alcohol before it goes on, and after the event, peel it off slowly.'])],  # E:1670569316:7
   faqs=[('Can our names and date be part of it?', 'Yes. Depending on the design, it can carry your initials, names and wedding date.'),  # E:1670569316:1
         ('Can it go on a window instead of a mirror?', 'Yes. Glass works the same way as a mirror.')],  # E:1670569316:24
   cap6=('A wreath on a venue door', 'A gold wreath decal on the glass entrance door of a venue.')),
 'large-format-event-graphics': dict(  # lean on purpose: gallery only (Steven, Nov 3 3:59 PM CT)
   cap6=('A wave down a venue hallway', 'A venue hallway with a floor-to-ceiling wave graphic and arrow shapes.')),
 'full-color-vinyl-prints': dict(
   sections=[('app-window', 'See-through window prints', ['See-through window prints come 18 x 24, 20 x 30, 24 x 36 or 24 x 48 inch.',  # E:4606421608:5
                                                          'Your design shows from outside, and people inside can still see out.',  # E:4606421608:1
                                                          'Keep words at least 1 inch tall, since finer text is hard to read on perforated film.'])],  # E:4606421608:16
   faqs=[('Can you print photos and gradients?', 'Yes. Prints are full color, so photos and gradients stay in.'),  # E:4605958764:11; EX:full-color-vinyl-prints-1
         ('Can I send a photo from my phone?', 'Yes. Send the largest version you have, because a higher-resolution image prints sharper.')],  # E:4605955948:7
   cap6=('A window print from inside', 'A full-color window print seen from inside the shop, the street visible through it.')),
 'custom-vinyl-decals': dict(
   sections=[('quote', 'Walls', ['Quote and lettering decals come 12 or 14 inch wide, and the height follows the words.',  # E:4606411955:5
                                 'Skip textured walls and brick, because the letters need a smooth surface.']),  # E:4606411955:17
             ('frame', 'Windows', ['Removable window decals peel off the glass slowly from one edge when you are done.'])],  # E:4606259782:20
   faqs=[('Can I use my own words?', 'Yes. A family name, a quote, a saying or a short verse all work.')],  # E:4606411955:1
   cap6=('Leaves on a wall and window', 'A cut-vinyl leaf pattern on a painted wall, with small matching decals on the window beside it.')),
}

# Slide 6 alt text (Design Bot - CW PASS3-NOTES.md, Nov 3 4:06 PM CT). The slide shows only when ex-<slug>-6-1200.webp exists.
ALT6 = {'wall-murals': 'a swirl mural covering a cafe wall from floor to ceiling',
 'lobby-logo-decals': 'a cut-vinyl logo on a glass office door with the hallway visible beyond',
 'wayfinding-decals': 'arrow and icon decals on a stairwell landing wall',
 'window-graphics': 'a one-color logo on a shop door at dusk with the lit shop behind it',
 'store-hours-decals': 'an hours decal at eye level beside the door handle, lines shown as simple bars',
 'storefront-lettering': 'a matching door decal and two window panels across a three-pane storefront',
 'vehicle-lettering': 'a full-color see-through graphic on the back window of an SUV',
 'fleet-decals': 'four white trucks in a row, each with the same logo and a number spot shown as bars',
 'banners': 'a vinyl banner tied to a chain-link fence beside a sports field',
 'logo-stickers': 'kraft mailers and shopping bags sealed with round logo stickers in two sizes',
 'die-cut-stickers': 'a laptop lid and a water bottle with die-cut stickers, one bordered and one cut to edge',
 'dance-floor-decals': 'a cut-vinyl wreath lying flat on hardwood floorboards',
 'wedding-monograms': 'a gold wreath decal on the glass entrance door of a venue',
 'large-format-event-graphics': 'a floor-to-ceiling wave wall graphic with arrow shapes in a venue hallway',
 'full-color-vinyl-prints': 'a full-color perforated window print seen from inside the shop, with the street visible through it',
 'custom-vinyl-decals': 'a cut-vinyl leaf pattern on a painted wall, with small matching decals on the window beside it'}
