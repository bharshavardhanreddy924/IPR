document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const isExpanded = navLinks.classList.contains('active');
            mobileMenuBtn.setAttribute('aria-expanded', isExpanded);
        });

        // Close mobile menu when a link is clicked, especially for on-page links
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', (e) => {
                // If it's a dropdown toggle, don't close menu immediately
                const parentLi = link.parentElement;
                if (parentLi.classList.contains('dropdown')) {
                    // Toggle 'open' class for sub-menu display
                    if (window.innerWidth <= 991) { // Only for mobile view
                        e.preventDefault(); // Prevent navigation for main dropdown link
                        parentLi.classList.toggle('open');
                        // Toggle submenu visibility directly
                        const subMenu = parentLi.querySelector('.dropdown-menu');
                        if (subMenu) {
                            subMenu.style.display = parentLi.classList.contains('open') ? 'block' : 'none';
                        }
                        return; // Stop further processing
                    }
                }

                if (navLinks.classList.contains('active')) {
                    // For actual navigation links (not just dropdown toggles)
                    if (!parentLi.classList.contains('dropdown') || window.innerWidth > 991) {
                         navLinks.classList.remove('active');
                         mobileMenuBtn.setAttribute('aria-expanded', 'false');
                    }
                }
            });
        });
    }

    // Smooth scroll for on-page links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href.length > 1 && document.querySelector(href)) {
                e.preventDefault();
                const targetElement = document.querySelector(href);
                if (targetElement) {
                     const offsetTop = targetElement.getBoundingClientRect().top + window.pageYOffset - 80; // Adjust 80 for sticky nav height
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
                // Close mobile nav if open (redundant with above, but safe)
                if (navLinks && navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                    mobileMenuBtn.setAttribute('aria-expanded', 'false');
                }
            }
        });
    });

    // Update current year in footer
    const currentYearEl = document.getElementById('currentYear');
    if (currentYearEl) {
        currentYearEl.textContent = new Date().getFullYear();
    }

    // TOC link highlighting based on scroll position (optional enhancement)
    const tocLinks = document.querySelectorAll('.toc a');
    const sections = [];
    tocLinks.forEach(link => {
        const targetId = link.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
            sections.push(targetElement);
        }
    });

    function highlightTocLink() {
        if(sections.length === 0 || tocLinks.length === 0) return;

        let currentSectionId = '';
        const scrollPosition = window.pageYOffset + (window.innerHeight / 3); // A bit down the viewport

        sections.forEach(section => {
            if (section.offsetTop <= scrollPosition) {
                currentSectionId = section.id;
            }
        });

        tocLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').substring(1) === currentSectionId) {
                link.classList.add('active');
            }
        });
    }
    // Add active class to TOC links
    if (tocLinks.length > 0) {
        tocLinks.forEach(link => {
            link.addEventListener('click', function() {
                tocLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');
            });
        });
        window.addEventListener('scroll', highlightTocLink);
        highlightTocLink(); // Initial call
    }
});