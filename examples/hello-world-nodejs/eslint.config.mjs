import globals from "globals";

export default [{
    languageOptions: {
        globals: {
            ...globals.node,
        },
    },

    rules: {
        camelcase: "error",
        "no-unused-vars": "error",
    },
}];