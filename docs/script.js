// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Preloader
    const preloader = document.createElement('div');
    preloader.className = 'preloader';
    preloader.innerHTML = '<div class="loader"></div>';
    document.body.appendChild(preloader);

    // Hide preloader when page is loaded
    window.addEventListener('load', function() {
        preloader.classList.add('fade-out');
        setTimeout(() => {
            preloader.remove();
        }, 500);
    });

    // Initialize AOS (Animate on Scroll)
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true,
            mirror: false
        });
    }

    // Update copyright year to always show 2025
    document.querySelectorAll('.copyright-year').forEach(element => {
        element.textContent = '2025';
    });
    // Back to top button functionality
    const backToTopButton = document.createElement('a');
    backToTopButton.href = '#';
    backToTopButton.className = 'back-to-top';
    backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
    document.body.appendChild(backToTopButton);

    // Show/hide back to top button based on scroll position
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block';
            setTimeout(() => {
                backToTopButton.style.opacity = '1';
            }, 10);
        } else {
            backToTopButton.style.opacity = '0';
            setTimeout(() => {
                backToTopButton.style.display = 'none';
            }, 300);
        }

        // Add parallax effect to hero section
        const heroSection = document.querySelector('.hero');
        if (heroSection) {
            const scrollPosition = window.pageYOffset;
            heroSection.style.backgroundPosition = `center ${scrollPosition * 0.4}px`;
        }

        // Animate elements when they come into view
        const animateElements = document.querySelectorAll('.animate-on-scroll');
        animateElements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            if (elementPosition < windowHeight - 100) {
                element.classList.add('animated');
            }
        });
    });

    // Smooth scroll to top when button is clicked
    backToTopButton.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Smooth scroll for all anchor links
    document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 70, // Adjust for fixed navbar
                    behavior: 'smooth'
                });
            }
        });
    });

    // Dark mode toggle
    const darkModeToggle = document.createElement('button');
    darkModeToggle.className = 'dark-mode-toggle';
    darkModeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    darkModeToggle.title = 'Toggle Dark Mode';
    document.body.appendChild(darkModeToggle);

    // Check for saved dark mode preference or system preference
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    if (localStorage.getItem('darkMode') === 'enabled' || (prefersDarkScheme.matches && !localStorage.getItem('darkMode'))) {
        document.body.classList.add('dark-mode');
        darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }

    // Toggle dark mode with animation
    darkModeToggle.addEventListener('click', function() {
        document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
        document.body.classList.toggle('dark-mode');

        if (document.body.classList.contains('dark-mode')) {
            localStorage.setItem('darkMode', 'enabled');
            darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
            darkModeToggle.classList.add('rotate-animation');
        } else {
            localStorage.setItem('darkMode', 'disabled');
            darkModeToggle.innerHTML = '<i class="fas fa-moon"></i>';
            darkModeToggle.classList.add('rotate-animation');
        }

        // Remove animation class after animation completes
        setTimeout(() => {
            darkModeToggle.classList.remove('rotate-animation');
        }, 500);
    });

    // Listen for system preference changes
    prefersDarkScheme.addEventListener('change', e => {
        if (!localStorage.getItem('darkMode')) {
            if (e.matches) {
                document.body.classList.add('dark-mode');
                darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
            } else {
                document.body.classList.remove('dark-mode');
                darkModeToggle.innerHTML = '<i class="fas fa-moon"></i>';
            }
        }
    });

    // Terminal typing effect with sequential animation
    const terminalResponses = document.querySelectorAll('.terminal-response');
    terminalResponses.forEach(response => {
        // Add typing animation class to the first paragraph
        const firstParagraph = response.querySelector('p');
        if (firstParagraph) {
            firstParagraph.classList.add('typing-animation');

            // Animate terminal response when it comes into view
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        firstParagraph.style.animationPlayState = 'running';
                        observer.unobserve(firstParagraph);
                    }
                });
            }, { threshold: 0.5 });

            observer.observe(firstParagraph);
        }
    });

    // Add copy functionality to code blocks
    document.querySelectorAll('.code-block').forEach(block => {
        // Create copy button
        const copyButton = document.createElement('button');
        copyButton.className = 'btn btn-sm btn-outline-light position-absolute top-0 end-0 m-2';
        copyButton.innerHTML = '<i class="fas fa-copy"></i>';
        copyButton.title = 'Copy to clipboard';

        // Set relative position on code block container
        block.style.position = 'relative';

        // Add button to code block
        block.appendChild(copyButton);

        // Add click event
        copyButton.addEventListener('click', () => {
            const textToCopy = block.textContent.trim();
            navigator.clipboard.writeText(textToCopy)
                .then(() => {
                    copyButton.innerHTML = '<i class="fas fa-check"></i>';
                    copyButton.classList.add('btn-success');
                    copyButton.classList.remove('btn-outline-light');
                    setTimeout(() => {
                        copyButton.innerHTML = '<i class="fas fa-copy"></i>';
                        copyButton.classList.remove('btn-success');
                        copyButton.classList.add('btn-outline-light');
                    }, 2000);
                })
                .catch(err => {
                    console.error('Failed to copy text: ', err);
                    copyButton.innerHTML = '<i class="fas fa-times"></i>';
                    copyButton.classList.add('btn-danger');
                    copyButton.classList.remove('btn-outline-light');
                    setTimeout(() => {
                        copyButton.innerHTML = '<i class="fas fa-copy"></i>';
                        copyButton.classList.remove('btn-danger');
                        copyButton.classList.add('btn-outline-light');
                    }, 2000);
                });
        });
    });

    // Add animation to navbar on scroll
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 100) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }

    // Add active class to nav items based on scroll position
    const sections = document.querySelectorAll('section[id]');
    window.addEventListener('scroll', function() {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionHeight = section.offsetHeight;
            if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });

        document.querySelectorAll('.navbar .nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}` ||
                (link.getAttribute('href') === 'index.html' && current === '')) {
                link.classList.add('active');
            }
        });
    });

    // Newsletter form submission
    const newsletterForm = document.querySelector('.footer form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const emailInput = this.querySelector('input[type="email"]');
            if (emailInput && emailInput.value) {
                // Show success message
                const successMessage = document.createElement('div');
                successMessage.className = 'alert alert-success mt-2';
                successMessage.textContent = 'Thank you for subscribing!';
                this.appendChild(successMessage);
                emailInput.value = '';

                // Remove message after 3 seconds
                setTimeout(() => {
                    successMessage.remove();
                }, 3000);
            }
        });
    }
});

// Add CSS class for animation
document.head.insertAdjacentHTML('beforeend', `
<style>
.rotate-animation {
    animation: rotate-icon 0.5s ease-in-out;
}

@keyframes rotate-icon {
    0% { transform: rotate(0); }
    100% { transform: rotate(360deg); }
}

.navbar-scrolled {
    background-color: rgba(10, 88, 202, 0.98) !important;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1) !important;
    padding-top: 5px !important;
    padding-bottom: 5px !important;
}

body.dark-mode .navbar-scrolled {
    background-color: rgba(13, 17, 23, 0.98) !important;
}
</style>
`);
