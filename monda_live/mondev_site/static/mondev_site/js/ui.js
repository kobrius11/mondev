console.log("MoNDA UI features loaded");

async function json_get(url) {
    const response = await fetch(url);
    const json = response.json();
    return json;
};

async function monda_collapse(obj_id) {
    const data = await json_get(sidebar_state_closed_url);
    if (data.state == 0) {
        const collapsible = document.getElementById(obj_id + "-content");
        const collapse_button = document.getElementById(obj_id + "-collapse");
        const uncollapse_button = document.getElementById(obj_id + "-uncollapse");
        collapsible.classList.add("hidden");
        collapse_button.classList.remove("block");
        collapse_button.classList.add("hidden");
        uncollapse_button.classList.remove("hidden");
        uncollapse_button.classList.add("block");
    };
};

async function monda_uncollapse(obj_id) {
    const data = await json_get(sidebar_state_open_url);
    if (data.state == 1) {
        const collapsible = document.getElementById(obj_id + "-content");
        const collapse_button = document.getElementById(obj_id + "-collapse");
        const uncollapse_button = document.getElementById(obj_id + "-uncollapse");
        collapsible.classList.remove("hidden");
        collapse_button.classList.remove("hidden");
        collapse_button.classList.add("block");
        uncollapse_button.classList.remove("block");
        uncollapse_button.classList.add("hidden");
    };
};

async function active_button(obj_id) {
    const uncollapsible = document.getElementById(obj_id);
    if (uncollapsible.classList.contains("active")) {
        uncollapsible.classList.remove("active");
    } else {
        uncollapsible.classList.add("active");
    };
};
