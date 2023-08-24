odoo.define("g2p_registry_base.CharToBadgePills", function (require) {
    var basicFields = require("web.basic_fields");
    var fieldRegistry = require("web.field_registry");
    const core = require("web.core");
    const QWeb = core.qweb;

    const CharToBadgePills = basicFields.DebouncedField.extend({
        className: "char_badge_pills",
        supportedFieldTypes: ["char"],

        init: function () {
            this._super.apply(this, arguments);
            this.separator = "|";
            this.confirmKeys = [$.ui.keyCode.ENTER, $.ui.keyCode.COMMA];
            this.tagClass = "badge badge-pill";
            this.options = {
                ...this.nodeOptions,
                tagClass: this.tagClass,
                confirmKeys: this.confirmKeys,
            };
        },

        _renderReadonly: function () {
            // Renders the field in readonly mode, displaying tags as badges
            const tags = this._getTagsValue();
            const html = QWeb.render("CharFieldTagsReadOnly", {
                tagClassFunction: this._tagClassFunction.bind(this),
                tags: tags,
            });
            this.$el.html(html);
        },

        _renderEdit: function () {
            // Renders the field in edit mode, allowing tags to be edited
            if (this.$input) {
                return;
            }
            this.$input = $("<select multiple/>");
            const tags = this._getTagsValue();
            for (const tag of tags) {
                this.$input.append($(`<option value="${tag}">${tag}</option>`));
            }
            this.$el.append(this.$input);
        },

        _setupTagsInput: function () {
            // Initializes the input field for tag input
            if (!this.$input) {
                return;
            }
            this.$input.tagsinput(this.options);
            this.$input.on("itemAdded", this._onAdd.bind(this));
            this.$input.on("itemRemoved", this._onRemove.bind(this));
            this.$tagsInput = this.$(".bootstrap-tagsinput");
            this.$tagsInputPlaceholder = this.$tagsInput.find("[placeholder]");
            this.$tagsInput.on("keyup", this._onKeyUp.bind(this));
        },

        on_attach_callback: function () {
            // Called when the field is attached to the DOM, sets up tag input
            this._setupTagsInput();
        },

        _onAdd: function () {
            // Called when a tag is added, triggers an action (e.g., saving)
            this._doAction();
        },

        _onRemove: function () {
            // Called when a tag is removed, triggers an action (e.g., saving)
            this._doAction();
        },

        _onKeyUp: function (e) {
            // Handles keyup events (e.g., Enter or comma) for tag input
            if (this.confirmKeys.includes(e.which)) {
                const value = this.$tagsInputPlaceholder.val();
                // Split the value using commas and trim each tag
                const tagsArray = value.split(",").map((tag) => tag.trim());

                for (const tag of tagsArray) {
                    if (tag !== "") {
                        this._addTag(tag);
                    }
                }

                this.$tagsInputPlaceholder.val("");
            }
        },

        _addTag: function (value) {
            // Adds a tag to the input field
            this.$input.tagsinput("add", value);
        },

        _removeTag: function (value) {
            // Removes a tag from the input field
            this.$input.tagsinput("remove", value);
        },

        _removeAll: function () {
            // Removes all tags from the input field
            this.$input.tagsinput("removeAll");
        },

        _getTagsValue: function () {
            // Retrieves the tags from the saved value and returns them as an array
            const savedValue = this.value || "";
            const tags = savedValue.split(",").map((tag) => tag.trim());
            return tags.filter((item) => item);
        },

        _getValue: function () {
            // Retrieves the tags from the input field and returns them as a string
            const input_value = this.$input.val();
            const tags = input_value.filter((item) => item);
            return tags.join(",");
        },

        _tagClassFunction: function () {
            // Generates CSS classes for styling tags
            return `badge badge-pill`;
        },
    });

    fieldRegistry.add("char_badge_pills", CharToBadgePills);

    return CharToBadgePills;
});
