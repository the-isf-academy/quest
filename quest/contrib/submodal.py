from quest.text_label import TextLabelStack

# A submodal should return True from `choose_option` when it has completed.
# That might be confusing for other readers. So instead, import CLOSE_SUBMODAL
# and return that.
CLOSE_SUBMODAL = True

class SubmodalMixin:
    """Extends `quest.modal.Modal` so that it can support submodals.

    Sometimes a modal needs to go into a deeper level of detail. For example
    an inventory list might need to present more details about a specific item.
    This could all be implemented within one modal, but it would get complicated
    quickly. Instead, `SubmodalMixin` allows a `Modal` to delegate its methods
    to another modal. The top-level modal remains in control and is the only modal 
    which actually gets rendered; any others are just used to access data and to 
    figure out how to respond to choices. 

    A modal which mixes in `SubmodalMixin` will check to see whether it has the 
    property `submodal` assigned before getting its text labels, option labels, or 
    choosing an option. When a submodal is present, that modal's behavior is called 
    instead of the modal. (That submodal could have its own submodals!)
    When a submodal is ready to be closed, it should return True (or CLOSE_SUBMODAL)
    from `choose_option` to signal the parent modal that it should resume control.

    Attributes:
        submodal (Modal): The current submodal (if any). 
    """

    submodal = None

    def set_text_labels(self):
        """Creates text labels.
        """
        text = (self.submodal or self).text_label_contents()
        self.text_labels = TextLabelStack(
            text,
            self.x_center,
            self.y_center + self.height / 2
        )

    def set_option_labels(self):
        """Creates option labels. 
        """
        options = (self.submodal or self).option_label_contents()
        disposable_stack = TextLabelStack(options, 0, 0)
        self.option_labels = TextLabelStack(
            options,
            self.x_center,
            self.y_center - self.height / 2 + disposable_stack.height()
        )
        self.current_option = 0
        self.option_labels.set_highlight(self.current_option)

    def handle_choice(self):
        "Lets submodal choose option, if set"
        if self.submodal:
            result = self.submodal.choose_option(self.current_option)
            if result:
                self.submodal = None
        else:
            result = self.choose_option(self.current_option)
        self.set_text_labels()
        self.set_option_labels()
