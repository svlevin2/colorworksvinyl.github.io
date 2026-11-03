"""Examples for the 16 product pages: (title, 1-2 sentence body). Approved by COO - CW 2026-11-03 10:37 CT (text as in e3d634c); shown while EXAMPLES_APPROVED is True.
The CW_EXAMPLES_PREVIEW=1 preview switch is no longer needed (flag is on); kept harmless for old preview scripts.
Source of record: /home/box/shared/colorworks/website/2026-11-03_pass2-examples-draft.md (generated from this file by tools/examples_md.py).
Photo per example: ex-<slug>-<n> (Design Bot); gradient icon art until each lands. Each body says what the piece is and what it is for (COO 10:30 CT). Vinyl only: no prices, materials, brands, sizes, durability or turnaround."""
import os
EXAMPLES_APPROVED = True or os.environ.get('CW_EXAMPLES_PREVIEW') == '1'  # COO - CW approved the text as written in e3d634c (2026-11-03 10:37 CT)
EXAMPLES = {
 'wall-murals': [
  ('A feature wall with your logo and brand colors', 'Your logo and colors in vinyl on a lobby, office or shop wall, so the space feels like your brand the moment people walk in.'),
  ('A mural for a cafe, gym or salon wall', 'Tell us your idea and we make the vinyl mural to fit your wall, so customers have something to look at while they visit.'),
  ("A wall graphic for a classroom or kids' room", 'Letters, shapes or a scene in vinyl for a classroom, nursery or play area, to make the room bright and welcoming for kids.'),
  ('A wall graphic made from your photo or artwork', 'Send us a photo or a piece of art and we turn it into a vinyl wall graphic, so a favorite image becomes part of the room.'),
  ('Your mission or a favorite quote as wall lettering', 'Your mission, values or a favorite quote in vinyl lettering, so your team and visitors see what you stand for.')],
 'lobby-logo-decals': [
  ('Your logo and name on the wall behind the front desk', 'Your logo and business name in vinyl on the wall behind the front desk, so visitors know they are in the right place.'),
  ('A logo decal on a glass office door', 'Your logo in vinyl on the glass of an office or suite door, so visitors find your door in a shared hallway.'),
  ('Office and meeting room names on glass', 'Vinyl lettering on glass doors and walls, so people can find each room without asking.'),
  ('Your logo on a lobby window', 'Your logo in vinyl on a lobby or entry window, so people see who you are before they walk in.'),
  ('A welcome wall with your name and logo', 'Your name, logo and a short welcome in vinyl on the wall guests see first, so your brand is the first thing they notice.')],
 'wayfinding-decals': [
  ('Room names and numbers on doors', 'Vinyl room names and numbers on doors, so visitors find the right room.'),
  ('Arrows and directions on hallway walls', 'Vinyl arrows and directions on hallway walls, so visitors get where they are going without asking.'),
  ('Restroom and office door decals', 'Vinyl decals that mark restrooms, offices and other doors, so guests can tell each door apart at a glance.'),
  ('Arrows that lead visitors to the front desk', 'A path of vinyl arrows from the entrance to your front desk, so first-time visitors go straight to check-in.'),
  ('Department names on walls', "Each department's name in vinyl on the wall outside its area, so people know which team they have reached.")],
 'window-graphics': [
  ('Your logo on the front window of a shop', 'Your logo in vinyl on the front window, so people spot your shop from the street.'),
  ('Your business name across a glass door', 'Your business name in vinyl across the glass of your front door, so customers know they found the right entrance.'),
  ('Window graphics for a salon or cafe', 'Vinyl window graphics in your colors for a salon, cafe or shop front, so your windows catch the eye of people walking by.'),
  ('Grand opening graphics for your windows', 'Vinyl window graphics that announce your grand opening, so neighbors and passersby know you are open.'),
  ('Your logo and website on an office front window', 'Your logo and website in vinyl on your office front window, so passersby know who you are and where to find you online.')],
 'store-hours-decals': [
  ('Your hours on the front door glass', 'Your opening hours in vinyl lettering on the front door glass, so customers know when to come in.'),
  ('Your phone and website under your hours', 'Add your phone number and website under your hours, so customers can reach you when the shop is closed.'),
  ('An hours decal for a salon, cafe or shop', 'An hours decal in vinyl in your colors and style, so your hours match the rest of your shop front.'),
  ('A new hours decal when your hours change', 'When your hours change, we make a new vinyl hours decal to match, so the door always shows your current hours.'),
  ('A QR code next to your hours', 'A vinyl QR code next to your hours that links to your website or menu, so customers can look you up even when you are closed.')],
 'storefront-lettering': [
  ('Your shop name on the front window', 'Your shop name in vinyl lettering across the front window, so people can find you from across the street.'),
  ('Salon services lettered on the window', 'A list of your salon services in vinyl lettering on the window, so people walking by see what you offer.'),
  ('Cafe menu items lettered on the glass', 'Your menu favorites in vinyl lettering on the cafe window, so passersby see what is good before they come in.'),
  ('Your office name and suite number on the door', 'Your office name and suite number in vinyl lettering on the door, so visitors find the right door.'),
  ('A short tagline on the door glass or the window above the door', 'A short line in vinyl lettering, so people know what you do as they walk up to your door.')],
 'vehicle-lettering': [
  ('Your business name and phone on truck doors', 'Your business name and phone number in vinyl on both truck doors, so people who see your truck know who to call.'),
  ('Your website on the back window', 'Your website in vinyl lettering on the back window, so drivers behind you can look you up.'),
  ('Lettering on the side windows of a van', 'Your business name and services in vinyl on the side windows of a van, so people know what you do as you drive by.'),
  ('Your services on a tailgate', 'A short list of your services in vinyl on the tailgate, so people at the job site or in the parking lot see what you do.'),
  ('A logo decal for a car door', 'Your logo as a vinyl decal on a car door, so your everyday car shows off your business wherever you park.')],
 'fleet-decals': [
  ('The same logo and lettering on every van', 'Your logo and lettering in vinyl, matched across every van, so customers recognize your company on any vehicle.'),
  ('Unit numbers on each vehicle', 'Vinyl unit numbers on each vehicle, so you and your team can tell them apart at a glance.'),
  ('Matching door lettering for a service fleet', 'The same vinyl door lettering on every service vehicle, so your team looks the same on every job.'),
  ('Lettering for a new vehicle that matches the rest', 'Adding a vehicle? We make vinyl lettering that matches the ones you already have, so the new one fits right in.'),
  ('Matching decals for trucks and vans', 'Matching vinyl decals for the trucks and vans in your fleet, so your brand looks the same whether a customer sees a truck or a van.')],
 'banners': [
  ('A grand opening banner for your storefront', 'A vinyl banner that tells people your doors are open, so new customers notice you right away.'),
  ('An event banner with sponsor logos', "A vinyl event banner with your event name and every sponsor's logo, so sponsors get seen and guests know they are in the right place."),
  ('A banner for your table at a fair or market', 'A vinyl banner for the front of your table at a fair, market or expo, so shoppers find your booth in a busy room.'),
  ('A sale or announcement banner', 'A vinyl banner for a sale, a new product or a big announcement, so people passing by hear the news.'),
  ('A welcome banner for a school or team event', 'A vinyl welcome banner for a school, team or community event, so families know they are in the right spot.')],
 'logo-stickers': [
  ('Logo stickers to seal your packaging', 'Logo stickers to seal boxes, bags and packages, so every order arrives with your brand on it.'),
  ('Stickers with a QR code for bags', 'Stickers with a QR code for your bags, so customers can find your website or menu later.'),
  ('Website stickers for shipping boxes', 'Stickers with your website for the outside of shipping boxes, so whoever gets the box knows where to order again.'),
  ('Logo stickers to hand out at events', 'Logo stickers to hand out at events, fairs and markets, so people take your name home with them.'),
  ('Stickers for product jars and boxes', 'Logo stickers for the lids and sides of product jars and boxes, so your products are easy to recognize on the shelf.')],
 'die-cut-stickers': [
  ('Stickers cut to the shape of your logo', 'Vinyl stickers cut around the outline of your logo, so your brand stands out on laptops, bottles and boxes.'),
  ('Mascot or character stickers', 'Stickers of your mascot or character, cut to its shape, for fans and customers to collect and share.'),
  ('Stickers with a white border', 'Die-cut stickers with a white border around the design, so the artwork stands out on dark or busy surfaces.'),
  ('Cut-to-edge stickers for laptops and water bottles', 'Stickers cut right to the edge of the design, so they look clean on laptops and water bottles.'),
  ('Team or event stickers in a custom shape', 'Stickers in a custom shape for your team, club or event, so members have something to show their pride.')],
 'dance-floor-decals': [
  ('Your initials and date in the middle of the dance floor', 'Your initials and wedding date in vinyl in the middle of the dance floor, so your first dance has a personal touch in every photo.'),
  ('A names and date decal for a wedding', 'A vinyl floor decal with both your names and the date, so your names are part of the party and the pictures.'),
  ('A logo floor decal for a company event', 'Your company logo as a vinyl floor decal for a party or company event, so your brand is center stage.'),
  ('A floor decal for a school dance or gala', 'A vinyl floor decal with the school or event name for a dance or gala, so the night feels like your own.'),
  ('An event name floor decal at the entrance', 'A vinyl floor decal with the event name at the entrance, so guests know they have arrived.')],
 'wedding-monograms': [
  ('A monogram decal for a welcome mirror', 'Your monogram in vinyl on a welcome mirror at the entrance, so guests know they are at the right celebration.'),
  ('Your names and date on a wall at the reception', 'Your names and wedding date in vinyl on a reception wall, so you have a personal backdrop for photos.'),
  ('A window decal with your monogram', 'Your monogram as a vinyl decal on a window at the venue, so your personal touch shows from inside and out.'),
  ('A Just Married decal for the getaway car window', 'Vinyl lettering for the back window of the getaway car, so everyone you pass knows you just got married.'),
  ('A monogram for the wall behind the cake table', 'Your monogram in vinyl on the wall behind the cake table, so the cake photos have a personal backdrop.')],
 'large-format-event-graphics': [
  ('Welcome graphics for an entry wall or door', 'Vinyl graphics with your event name and a welcome for an entry wall or door, so guests know they found the right event.'),
  ('Directional vinyl decals that guide guests to the room, bar or photo spot', 'Vinyl arrows and lettering that point guests the right way, so nobody has to ask for directions.'),
  ("Sponsor wall graphics with every sponsor's logo", "Vinyl wall graphics with every sponsor's logo in one place, so each sponsor is seen and guests have a spot for photos."),
  ('Stage and table-front vinyl graphics', 'Vinyl graphics for the front of the stage and the tables, so your event looks finished from every seat.'),
  ('Event name and logo graphics for a wall or window', 'Your event name and logo in vinyl for a wall or window, so your event name shows up in every photo.')],
 'full-color-vinyl-prints': [
  ('Full-color logo graphics with gradients or photos', 'Logo graphics printed on vinyl in full color, so a logo with gradients or photos keeps its look on walls and windows.'),
  ('Photo and artwork prints on vinyl for a wall', 'Your photo or artwork printed on vinyl for a wall, so the space shows off your work or your story.'),
  ('Full-color vinyl window graphics for a storefront', 'Full-color vinyl graphics for your storefront windows, so your shop stands out to people walking and driving by.'),
  ('Printed vinyl decals for a vehicle door or window', 'Full-color vinyl decals for a vehicle door or window, so your brand goes with you wherever you drive.'),
  ('Full-color vinyl sticker sheets for giveaways', 'Sheets of full-color vinyl stickers to hand out, for customers, kids or event guests to take home.')],
 'custom-vinyl-decals': [
  ('Logo decals for an office wall or front window', 'Your logo as a vinyl decal for an office wall or front window, so visitors know whose space they are in.'),
  ('Quote and lettering decals for a wall', 'A quote or lettering in vinyl for a wall at home or at work, to inspire everyone who walks past.'),
  ('Room-name and door decals', 'Vinyl room names and door decals for offices and homes, so everyone knows which door is which.'),
  ('Hours and info decals for a door', 'Vinyl decals with your hours, phone or website for a door, so customers can reach you even after hours.'),
  ('Car window decals with your logo or website', 'Your logo or website as a vinyl decal for a car window, so people see your business wherever you drive.')],
}
