# Synthara | The Education Times CLI Website

This directory contains the website for the Synthara | The Education Times CLI project.

## Setting up GitHub Pages

To host this website using GitHub Pages:

1. Go to your repository on GitHub
2. Click on "Settings"
3. Scroll down to the "GitHub Pages" section
4. Under "Source", select "main branch" and "/docs" folder
5. Click "Save"

Your website will be available at: https://bniladridas.github.io/gemini_cli/

## Custom Domain (Optional)

If you want to use a custom domain:

1. Purchase a domain name from a domain registrar
2. In your repository settings, under "GitHub Pages" > "Custom domain", enter your domain name
3. Update your domain's DNS settings to point to GitHub Pages:
   - Add an A record pointing to GitHub Pages IP addresses:
     - 185.199.108.153
     - 185.199.109.153
     - 185.199.110.153
     - 185.199.111.153
   - Or add a CNAME record pointing to `bniladridas.github.io`

The CNAME file in this directory is already set up for the domain `synthara.education`. Update it if you choose a different domain name.

## Local Development

To test the website locally:

1. Open the `index.html` file in your browser
2. Or use a local server:
   ```bash
   # Using Python
   python -m http.server
   
   # Using Node.js
   npx serve
   ```
