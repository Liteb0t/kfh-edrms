// Fuze Tables 1.0.2 - Library to display JSON data in a table
// Developed by https://fuze.page/
// License: MIT

class FuzeTable {
	// container_id is the contents of the "id" tag in
	// <div class="table-container" id="your-fuzetable-name"></div>
	constructor(container_id, config = {}) {
		var defaults = {
			title: "Fuze Table"
			,page: 1
			,entries_per_page: 10
			,json_path: ""
			,json_data: {}
			,included_data: {}
			,columns: {}
			,store_page_in_url: true
			,sort_column: "initial"
			,sort_order: "none"
			,column_maps: {}
			,clickable_rows: false
			,on_row_click: this.onRowClickDefault
			// ,sticky_headers: false
		}
		Object.assign(this, defaults, config);

		// Unique ID so several tables can have page stored in URL
		this.id = ++FuzeTable.id;
		this.url_identifier = `t${this.id}p`;
		this.column_maps = {};
		this.column_maps_search = {};
		this.searching_columns = [];

		this.linkToHTML(container_id);
		// this.setIndexRange();
		// this.error_message = "";


		if (Object.keys(this.json_data).length > 0) {
			console.log("Skipping loading JSON!");
			this.initializeTable();
			this.addColumnSorting();
			this.populateTable();
		}
		else if (this.json_path) {
			this.loadData(this.json_path)
				.then(() => {
					this.initializeTable();
					this.addColumnSorting();
					this.populateTable();
				});
		}
		else {
			console.log("No JSON provided!");
			this.table_tbody_element.innerHTML = "No data found."
			// To do later: show error in the table and still load title bar
		}
		// To do later: ensure there is no clash in URL page navigation names
	}

	linkToHTML(container_id) {
		this.container_element = document.getElementById(container_id);
		
		this.title_and_navigation_container_element = document.createElement("div");
		this.title_and_navigation_container_element.classList.add("table-title-and-navigation-container");
		this.container_element.appendChild(this.title_and_navigation_container_element);
		
		this.title_element = document.createElement("div");
		this.title_element.classList.add("table-title");
		
		this.showing_indexes_element = document.createElement("div");
		// this.showing_indexes_element.classList.add("showing-indexes");
	
		this.page_buttons_element = document.createElement("div");	

		this.title_and_navigation_container_element.appendChild(this.title_element);
		this.title_and_navigation_container_element.appendChild(this.showing_indexes_element);

		this.title_and_navigation_container_element.appendChild(this.page_buttons_element);

		// Page navigation buttons
		this.page_down_button_element = document.createElement("button");
		this.page_down_button_element.classList.add("page-button");
		this.page_down_button_element.style["display"] = "none";
		this.page_down_button_element.onclick = this.pageDown.bind(this);
		this.page_down_button_element.innerHTML = "Previous page";

		this.page_up_button_element = document.createElement("button");
		this.page_up_button_element.classList.add("page-button");
		this.page_up_button_element.style["display"] = "none";
		this.page_up_button_element.onclick = this.pageUp.bind(this);
		this.page_up_button_element.innerHTML = "Next page";

		this.page_buttons_element.appendChild(this.page_down_button_element);
		this.page_buttons_element.appendChild(this.page_up_button_element);

		// Table container element is required for making the
		// table scrollable if the screen is too small
		this.table_container_element = document.createElement("div");
		this.table_container_element.classList.add("table-container");
		this.container_element.appendChild(this.table_container_element);
	
		this.table_element = document.createElement("table");
		this.table_container_element.appendChild(this.table_element);

		this.table_thead_element = document.createElement("thead");
		this.table_element.appendChild(this.table_thead_element);
		
		this.table_tbody_element = document.createElement("tbody");
		this.table_element.appendChild(this.table_tbody_element);

		this.title_element.innerHTML = this.title;

		this.table_tbody_element.innerHTML = "Loading...";
	}

	async loadData(file_name) {
		let data = await fetch(file_name);
		// return data.json();
		this.json_data = await data.json();
		// self.included_data = self.json_data;
	}

	// Do a first-time preparation of the table. 
	// Called after we have the JSON but before populating the table
	// 
	initializeTable() {
		this.included_data = this.json_data;

		this.column_maps["initial"] = Array.from({length: this.included_data.length}, (e, i) => [i, i]);
		this.column_maps_search["initial"] = JSON.parse(JSON.stringify(this.column_maps["initial"]));

		// By default, every attribute in the JSON is displayed
		// with the property name.
		// The user can set a display name or hide the column

		let user_assigned_columns = this.columns;
		this.columns = {};
		Object.keys(this.json_data[0]).forEach(column_name => {
			// this.columns.column_name = { ...{display_name: column_name, visible: true}, ...this.columns.column_name };
			let default_value = {
				display_name: column_name
				,visible: true
				,type: "auto"
				,searching: false
				// ,mapped_values: []
				// ,element: ""
				// ,sorting_order: "none"
			}
			this.columns[column_name] = { ...default_value, ...user_assigned_columns[column_name]};
		});
		// this.columns = {...this.columns, ...user_assigned_columns}
		// console.log(this.columns);
		
		let tr = document.createElement("tr");
		this.table_thead_element.appendChild(tr);
	
		// add each ENABLED column header
		for (let [column_id, properties] of Object.entries(this.columns)) {
			if (properties.visible) {
				properties.element = document.createElement("th");
				tr.appendChild(properties.element);
				// properties.element.onclick = () => {this.sortColumn(column_id);}
				properties.element.appendChild(document.createTextNode(properties.display_name));
			}
		}
		// console.log(this.column_maps.initial);
		// this.column_maps_search["initial"] = this.column_maps["initial"];
	}

	addColumnSorting() {
		// this.column_maps_search["initial"] = this.column_maps["initial"];
		// add each ENABLED column header
		for (let [column_id, properties] of Object.entries(this.columns)) {
			if (properties.visible) {

				// console.log(column_id);
				
				// properties.element.onclick = () => {this.sortColumn(column_id);}

				this.column_maps[column_id] = [];
				// this.column_maps[column_id] = this.included_data.map((i) => [i[column_id]).sort();
				for (let i = 0; i < this.included_data.length; i++) {
					this.column_maps[column_id].push([this.included_data[i][column_id], i]);
				}
				// this.column_maps[column_id].sort((value, pointer) => {
				// 	return value[0]-pointer[0] // i dont understand this but it works
				// });
				if (this.columns[column_id].type == "auto" && 
					!isNaN(this.included_data[0][column_id])) {
					// Is a valid float (number)
					console.log(`Sorting ${column_id} with number algorithm`);
					this.column_maps[column_id].sort(FuzeTable.sortColumnMapNumber);
				}
				else {
					// Is a string
					console.log(`Sorting ${column_id} with string algorithm`);
					this.column_maps[column_id].sort(FuzeTable.sortColumnMapString);
				}
				this.column_maps_search[column_id] = JSON.parse(JSON.stringify(this.column_maps[column_id]));

				let temp_div = document.createElement("div");
				temp_div.classList.add("column-buttons");
				properties.element.appendChild(temp_div);

				properties.sort_button_element = document.createElement("span");
				// properties.sort_button_element.classList.add("column-button");
				properties.sort_button_element.innerHTML = "⇕" // ⇕
				properties.sort_button_element.onclick = () => {this.sortColumn(column_id);}
				temp_div.appendChild(properties.sort_button_element);
				
				properties.search_button_element = document.createElement("span");
				// properties.search_button_element.classList.add("column-button");
				properties.search_button_element.innerHTML = "🔍" // ⇕
				properties.search_button_element.onclick = () => {this.toggleSearchBar(column_id);}
				temp_div.appendChild(properties.search_button_element);

				properties.search_bar_element = document.createElement("input");
				properties.search_bar_element.placeholder = "Search...";
				properties.search_bar_element.style["display"] = "none";
				properties.search_bar_element.addEventListener("change", () => {this.doSearch()});
				properties.element.appendChild(properties.search_bar_element);
			}
		}
	}

	updateSearchColumnMaps() {
		if (typeof this.included_data[0] === "undefined") return;

		for (let [column_id, properties] of Object.entries(this.columns)) {
			if (properties.visible) {
			// console.log(column_id);
					// properties.element.onclick = () => {this.sortColumn(column_id);}

				this.column_maps_search[column_id] = [];
				// this.column_maps_search[column_id] = this.included_data.map((i) => [i[column_id]).sort();
				for (let i = 0; i < this.included_data.length; i++) {
					this.column_maps_search[column_id].push([this.included_data[i][column_id], i]);
				}
				// this.column_maps_search[column_id].sort((value, pointer) => {
				// 	return value[0]-pointer[0] // i dont understand this but it works
				// });
				if (this.columns[column_id].type == "auto" && 
					!isNaN(this.included_data[0][column_id])) {
					// Is a valid float (number)
					console.log(`Sorting ${column_id} with number algorithm`);
					this.column_maps_search[column_id].sort(FuzeTable.sortColumnMapNumber);
				}
				else {
					// Is a string
					console.log(`Sorting ${column_id} with string algorithm`);
					this.column_maps_search[column_id].sort(FuzeTable.sortColumnMapString);
				}
			}
		}
	}


	updateColumnSortButtons() {
		for (let [column_id, properties] of Object.entries(this.columns)) {
			if (properties.visible) {
				if (this.sort_column == "initial") {
					properties.sort_button_element.innerHTML = "⇳";
				}
				else if (this.sort_column == column_id && this.sort_order == "ascending") {
					properties.sort_button_element.innerHTML = "⇩";
				}
				else if (this.sort_column == column_id && this.sort_order == "descending") {
					properties.sort_button_element.innerHTML = "⇧";
				}
				else {
					properties.sort_button_element.innerHTML = "°";
				}
			}
		}
	}


	sortColumn(column_id) {
		// console.log("It worked :)");
		// console.log(column_id);
		if (this.sort_column != column_id) {
			this.sort_column = column_id;
			this.sort_order = "ascending";
		}
		else if (this.sort_order == "ascending") {
			this.sort_order = "descending";
		}
		else if (this.sort_order == "descending") {
			this.sort_order = "none";
			this.sort_column = "initial";
		}
		else {
			this.sort_order = "ascending";
		}
		this.populateTable();
		this.updateColumnSortButtons();
	}

	toggleSearchBar(column_id) {
		if (this.columns[column_id].searching) {
			// hide search bar
			// this.searching_columns.pop(column_id);
			this.columns[column_id].search_button_element.innerHTML = "🔍";
			this.columns[column_id].search_bar_element.style["display"] = "none";
			this.columns[column_id].searching = false;
			this.columns[column_id].search_bar_element.value = "";
			this.doSearch();
		}
		else {
			// show search bar
			this.columns[column_id].search_button_element.innerHTML = "❌";
			this.columns[column_id].search_bar_element.style["display"] = "inline-block";
			// this.searching_columns.push(column_id);
			this.columns[column_id].searching = true;
		}
	}

	doSearch() {
		// this.searching_columns.forEach(column => {
		// 	console.log(`I am searching ${column} !`);
		// });
		// console.log(e);
	
		this.included_data = JSON.parse(JSON.stringify(this.json_data));
		// this.column_maps_search["initial"] = this.column_maps["initial"];
		// this.included_data = this.json_data.forEach((item, index, fullArray) => {item.original_index = index});
		for (let [map_id, value] of Object.entries(this.column_maps)) {
			this.column_maps_search[map_id] = JSON.parse(JSON.stringify(value));
		}

		for (let [column_id, properties] of Object.entries(this.columns)
			.filter(([key, val]) => val.searching == true)) {
			console.log(`I am searching ${column_id} !`);

			for (let i = 0; i < this.included_data.length; i++) {
				if (!(typeof this.included_data[i] === "undefined")) {
					if (!(this.included_data[i][column_id].toLowerCase().includes(properties.search_bar_element.value.toLowerCase()))) {
						delete this.included_data[i];
						// delete this.column_maps_search["initial"][i];
					}
				}
			}

			// console.log(this.column_maps_search.initial);
			// this.column_maps_search[column_id] = this.column_maps_search[column_id].filter((e) => {return e != null});

			// this.column_maps_search["initial"] = this.column_maps_search["initial"].filter((e) => {return e != null});
			this.included_data = this.included_data.filter((e) => {return e != null});
		
			this.column_maps_search["initial"] = Array.from({length: this.included_data.length}, (e, i) => [i, i]);
		
			this.updateSearchColumnMaps();
		}
	
		// this.included_data = this.included_data.filter((e) => {return e != null});
		this.column_maps_search["initial"] = this.column_maps_search["initial"].filter((e) => {return e != null});
		for (const column_map in this.column_maps_search) {
			this.column_maps_search[column_map] = this.column_maps_search[column_map].filter((e) => {return e != null});
		}
		this.setPage(1);

		this.populateTable();

	}

	populateTable() {
		// let urlParams = new URLSearchParams(window.location.search)
		const url = new URL(window.location.href);
		if (url.searchParams.get(this.url_identifier)) {
			this.page = Number(url.searchParams.get(this.url_identifier));
		}
		this.setIndexRange();
		this.loadPageNavigation();
		// To do later: add error message if indexes are outside of bounds

		let // start_index = this.show_from_index,
			// stop_index = this.show_to_index,
			increment = 1;

		if (this.sort_order == "descending") {
	
			increment = -1;
		}

		// console.log(`show_from_index: ${this.show_from_index}\nshow_to_index: ${this.show_to_index}\nincrement: ${increment}`);

		this.table_tbody_element.innerHTML = "";

		for (let i = this.show_from_index_sorted; i != this.show_to_index_sorted; i += increment) {
			let tr = document.createElement("tr");
			this.table_tbody_element.appendChild(tr);
		
			// console.log(`I: ${i}`);
			// Now loop through company attributes
			// for (var key in company) {
			for (let [column_id, properties] of Object.entries(this.columns)) {
				if (properties.visible) {
					let td = document.createElement("td");
					tr.appendChild(td);
					// console.log(col);
					// console.log(i);
					td.appendChild(document.createTextNode(
						this.included_data[this.column_maps_search[this.sort_column][i][1]][column_id]
					));
					if (this.clickable_rows) {
						// call the on_row_click function, 
						// passing the INDEX of included_data value
						td.addEventListener("click", () => this.on_row_click(this.column_maps_search[this.sort_column][i][1]));
					}
				}
			}
		}
		// if (this.clickable_rows) {
		// 	// Make table rows clickable
		// 	for (var i = 0, row; i < this.table_element.rows.length; i++) {
		// 		const row_id = table.rows[i].id;
		// 		table.rows[i].addEventListener("click", () => {
		// 			// When a table row is clicked, go to details page with that employee ID
		// 			window.location.href = `details/${row_id}`;
		// 	    })
		// 	}
	}

	onRowClickDefault(index) {
		console.log(`Row clicked! index: ${index}`);
	}

	setPage(page, ignoreURL = false) {
		if (ignoreURL == false) {
			const url = new URL(window.location.href);
			url.searchParams.set(this.url_identifier, page);
			history.pushState({}, null, url.search);
		}
		this.page=page;
		this.populateTable();
	}

	pageUp() {
		console.log("did PageUp");
		console.log(`this.page is ${this.page}`);
		this.setPage((++this.page));
	}
	pageDown() {
		this.setPage((--this.page));
		console.log("did PageUp");
		console.log(`this.page is ${this.page}`);
	}

	loadPageNavigation() {

		this.showing_indexes_element.innerHTML = `Showing ${this.show_from_index + 1} - ${this.show_to_index} of ${this.included_data.length}`;

		if (this.page > 1) {
			this.page_down_button_element.style["display"] = "inline-block";
			// this.page_down_button_element.onclick = this.setPage(this.page - 1);
		}
		else {
			this.page_down_button_element.style["display"] = "none";
		}


		if (this.page < this.included_data.length / this.entries_per_page) {
			this.page_up_button_element.style["display"] = "inline-block";
		}
		else {
			this.page_up_button_element.style["display"] = "none";
		}
	}

	setIndexRange() {
		console.log(this.sort_column);
		console.log(this.column_maps);
		console.log(this.column_maps[this.sort_column]);


		this.show_from_index = (this.page - 1) * this.entries_per_page;
		this.show_to_index = this.show_from_index + this.entries_per_page;
		

		// stay within range of included JSON data
		// if (this.show_to_index > this.included_data.length) {
		// 	this.show_to_index = this.included_data.length;
		// }
		if (this.show_to_index > this.column_maps_search[this.sort_column].length) {
			this.show_to_index = this.column_maps_search[this.sort_column].length;
		}
		if (this.show_from_index < 0) {
			this.show_from_index = 0;
		}

		if (this.sort_order == "descending") {
			// this.show_from_index = this.show_from_index ^ this.show_to_index;
			// this.show_to_index = this.show_from_index ^ this.show_to_index;
			// this.show_from_index = this.show_from_index ^ this.show_to_index;
			this.show_from_index_sorted = (this.column_maps_search[this.sort_column].length - 1) - this.show_from_index;
			this.show_to_index_sorted = this.column_maps_search[this.sort_column].length - (this.show_to_index+1);
		}
		else {
			this.show_from_index_sorted = this.show_from_index;
			this.show_to_index_sorted = this.show_to_index;
		}

	}

	static id = 0;

	static sortColumnMapString(value, included_data_index) {
		if (value[0] === included_data_index[0]) {
			return 0;
		}
		else {
			return (value[0].toLowerCase() < included_data_index[0].toLowerCase()) ? -1 : 1;
		}
	}

	static sortColumnMapNumber(value, included_data_index) {
		return parseFloat(value) - parseFloat(included_data_index);
		// return value - included_data_index;
	}
} 
