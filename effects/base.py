from clip_editor import ClipEditor

class Effect(): #Base class only used to define subclasses
    def apply(self, editor: ClipEditor):
        raise NotImplementedError("Effect class itself is not used; its subclasses must be, where this method will be overridden by it")
