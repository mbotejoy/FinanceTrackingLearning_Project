
document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("transactionForm");

    const transactionType = document.getElementById("id_type");
    const category = document.getElementById("id_category");
    const subcategory = document.getElementById("id_subcategory");

    const subcategorySection = document.getElementById("subcategorySection");

    const addButton = document.getElementById("addSubcategoryBtn");
    const newForm = document.getElementById("newSubcategoryForm");

    const nameInput = document.getElementById("newSubcategoryName");

    const saveButton = document.getElementById("saveSubcategoryBtn");
    const cancelButton = document.getElementById("cancelSubcategoryBtn");

    const message = document.getElementById("subcategoryMessage");

    const getUrl = form.dataset.getSubcategoriesUrl;
    const addUrl = form.dataset.addSubcategoryUrl;

    // Keep a copy of all categories before filtering.
    const allCategoryOptions = Array.from(category.options)
        .filter(option => option.value !== "")
        .map(option => option.cloneNode(true));

    // Match transaction types to category types.
    const categoryTypeMapping = {
        "income/allowance": "income",
        "expense": "expense",
        "savings": "savings",
        "investment": "investment",
        "debt_repayment": "debt_repayment"
    };

    function showMessage(text, isError = false) {
        message.textContent = text;
        message.style.color = isError ? "red" : "green";
    }

    // Filter categories according to the selected transaction type.
    function filterCategories(clearSelection = false) {

        const selectedType = transactionType.value;

        const expectedCategoryType = categoryTypeMapping[selectedType];

        const previousCategory = clearSelection ? "" : category.value;

        category.innerHTML = "";

        const placeholder = document.createElement("option");
        placeholder.value = "";
        placeholder.textContent = "Select a category";

        category.appendChild(placeholder);

        allCategoryOptions.forEach(function (option) {

            // Category labels are displayed as Name (type).
            const match = option.textContent.trim().match(/\(([^()]*)\)$/);

            if (!match) {
                return;
            }

            const categoryType = match[1].trim().toLowerCase();

            if (categoryType === expectedCategoryType) {

                const newOption = option.cloneNode(true);

                category.appendChild(newOption);
            }

        });

        // Preserve the category when initially loading an edit form.
        if (previousCategory) {
            category.value = previousCategory;
        }

        // If the previous category does not match, clear it.
        if (category.value !== previousCategory && previousCategory) {
            category.value = "";
        }
    }

    function resetSubcategories() {

        subcategory.innerHTML = "";

        const placeholder = document.createElement("option");
        placeholder.value = "";
        placeholder.textContent = "Select a subcategory (optional)";

        subcategory.appendChild(placeholder);
    }

    async function loadSubcategories() {

        resetSubcategories();
        showMessage("");

        const selectedType = transactionType.value;
        const selectedCategory = category.value;

        if (selectedType !== "expense" || !selectedCategory) {
            subcategorySection.style.display = "none";
            return;
        }

        subcategorySection.style.display = "block";

        try {

            const response = await fetch(
                `${getUrl}?category=${encodeURIComponent(selectedCategory)}`
            );

            if (!response.ok) {
                throw new Error("Unable to load subcategories.");
            }

            const data = await response.json();

            data.forEach(function (item) {

                const option = document.createElement("option");

                option.value = item.id;
                option.textContent = item.name;

                subcategory.appendChild(option);

            });

        } catch (error) {

            showMessage(
                "Could not load subcategories. Please try again.",
                true
            );

        }
    }

    // Update categories when transaction type changes.
    transactionType.addEventListener("change", function () {

        filterCategories(true);
        loadSubcategories();

    });

    // Update subcategories when category changes.
    category.addEventListener("change", loadSubcategories);

    addButton.addEventListener("click", function () {

        if (transactionType.value !== "expense" || !category.value) {
            showMessage(
                "Please select an expense category first.",
                true
            );
            return;
        }

        newForm.style.display = "block";
        nameInput.focus();

    });

    cancelButton.addEventListener("click", function () {

        newForm.style.display = "none";
        nameInput.value = "";
        showMessage("");

    });

    saveButton.addEventListener("click", async function () {

        const name = nameInput.value.trim();

        if (!name) {
            showMessage("Please enter a subcategory name.", true);
            return;
        }

        if (!category.value || transactionType.value !== "expense") {
            showMessage("Please select an expense category first.", true);
            return;
        }

        const csrfToken = form.querySelector(
            "[name=csrfmiddlewaretoken]"
        ).value;

        const formData = new FormData();

        formData.append("category", category.value);
        formData.append("name", name);
        formData.append("csrfmiddlewaretoken", csrfToken);

        saveButton.disabled = true;
        saveButton.textContent = "Saving...";

        try {

            const response = await fetch(addUrl, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": csrfToken
                }
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(
                    data.message || "Could not save subcategory."
                );
            }

            const option = document.createElement("option");

            option.value = data.id;
            option.textContent = data.name;
            option.selected = true;

            subcategory.appendChild(option);

            newForm.style.display = "none";
            nameInput.value = "";

            showMessage(data.message);

        } catch (error) {

            showMessage(error.message, true);

        } finally {

            saveButton.disabled = false;
            saveButton.textContent = "Save Subcategory";

        }

    });

    // Filter categories first, then load existing subcategories.
    // This also supports editing an existing transaction.
    filterCategories(false);
    loadSubcategories();

});
