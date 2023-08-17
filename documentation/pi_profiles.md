
Adding videos to user profile pages
===================================

1. Find the URL for the video
   - View the video on the page where it is referenced in the Drupal system
   - Click on the "Watch on Youtube" in the lower-left of the video
   - Once Youtube starts playing the video, copy the video's ID from the address bar
     (the part after "watch?v=")
   - Use the ID to create the video's embedded URL:
	 https://www.youtube.com/embed/ID_GOES_HERE?autoplay=0&start=0&rel=0
2. Find the user's profile ID in CIC
   - Go to the person administration page
     https://cic-apps.datascience.columbia.edu/admin/apis/person/
   - Search for the person's name
   - Click on the name to go into editing mode
   - In the address bar, note the ID number that comes after /person
3. Create a new Asset object for the video
   - Go to the Add Asset page
	 https://cic-apps.datascience.columbia.edu/admin/apis/asset/add/
   - For the Filename, enter cic_video
   - For the Download path, enter the Youtube URL you constructed in step 1
   - For the Author, enter the number you obtained from step 2
   - Ensure the Approved box is checked, and leave everything else blank
   - Click the Save button
   - Go to the author's profile and ensure the video displays properly

