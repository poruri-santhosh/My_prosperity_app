document.addEventListener("DOMContentLoaded", () => {

    // ==============================
    // Load Tableau Visualization
    // ==============================
    const loadTableauViz = (div) => {
        const vizElement = div.getElementsByTagName('object')[0];
        if (!vizElement) return;

        // Force responsive scaling
        vizElement.style.width = '100%';
        vizElement.style.height = '100%';

        const script = document.createElement('script');
        script.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';

        script.onload = () => {
            setTimeout(() => {

                // Remove loader if exists
                const card = div.closest('.dashboard-card');
                if (card) {
                    const overlay = card.querySelector('.skeleton-overlay');
                    if (overlay) {
                        overlay.style.opacity = '0';
                        setTimeout(() => overlay.remove(), 600);
                    }
                }

                // Force iframe to be fully responsive
                const iframe = div.querySelector('iframe');
                if (iframe) {
                    iframe.style.width = '100%';
                    iframe.style.height = '100%';
                    iframe.style.position = 'absolute';
                    iframe.style.top = '0';
                    iframe.style.left = '0';
                }

            }, 2500); // wait for Tableau to render
        };

        vizElement.parentNode.insertBefore(script, vizElement);
    };

    // ==========================================
    // Intersection Observer (Lazy Load Tableau)
    // ==========================================
    const vizObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                loadTableauViz(entry.target);
                vizObserver.unobserve(entry.target);
            }
        });
    }, { 
        threshold: 0.1, 
        rootMargin: '0px 0px 400px 0px' 
    });

    document.querySelectorAll('.tableauPlaceholder')
        .forEach(div => vizObserver.observe(div));


    // ==========================================
    // Sidebar Active Section Highlight
    // (For analytics.html)
    // ==========================================
    const sections = document.querySelectorAll('section[id]');

    const navObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');

                document.querySelectorAll('.sidebar-link').forEach(link => {
                    const href = link.getAttribute('href').replace('#', '');
                    link.classList.toggle('active', href === id);
                });
            }
        });
    }, { threshold: 0.4 });

    sections.forEach(section => navObserver.observe(section));

});
