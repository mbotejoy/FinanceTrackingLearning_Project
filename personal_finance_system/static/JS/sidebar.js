const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebar-toggle');
const mainContent = document.getElementById('mainContent');

//This function is run each time a user clicks the sidebar toggle button. 
sidebarToggle.addEventListener('click', () => {
    // Adds or removes the "collapsed" class from the sidebar.
    // It returns true when the class was added and false when removed.
    const isCollapsed = sidebar.classList.toggle("collapsed");

    // Adds "expanded" to the main content only when the sidebar is collapsed.
    // This lets the main content move left and use the available space.
    mainContent.classList.toggle("expanded", isCollapsed);

    // Updates the accessibility attribute for screen-reader users.
    // aria-expanded is "false" when the sidebar is collapsed.
    sidebarToggle.setAttribute("aria-expanded", String(!isCollapsed));
});

