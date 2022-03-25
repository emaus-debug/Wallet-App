const searchField = document.querySelector('#searchField');
const tableOutput = document.querySelector('.table-output');
const appTable = document.querySelector('.app-table');
const paginationContainer = document.querySelector('.pagination-container');
const noResults = document.querySelector(".no-results");
const tableBody = document.querySelector('.table-body');

tableOutput.style.display = "none";


searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
        paginationContainer.style.display = "none";
        tableBody.innerHTML = "";

        fetch('/budgets/search-element', {
                body: JSON.stringify({ searchText: searchValue }),
                method: "POST",
                headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
            }).then((res) => res.json())
            .then((data) => {
                console.log('data', data);
                appTable.style.display = "none";
                tableOutput.style.display = "block";

                console.log("data.length", data.length);

                if (data.length === 0) {
                    noResults.style.display = "block";
                    tableOutput.style.display = "none";
                } else {
                    noResults.style.display = "none";
                    data.forEach((item) => {
                        tableBody.innerHTML += `
                            <tr>
                                <td>${item.designation}</td>
                                <td>${item.prix_unitaire}</td>
                                <td>${item.quantite}</td>
                                <td>${item.description}</td>
                                <td>${item.total}</td>
                                <td>${item.status}</td>
                            </tr>`;
                    });
                }
            });
    } else {
        tableOutput.style.display = "none";
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
    }
});