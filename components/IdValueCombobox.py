
import ttkbootstrap as ttb

class Combobox(ttb.Combobox):
    def __init__(self, master, data, variable, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.__variable: ttb.IntVar = variable
        
        self.values = []
        self.idValues = []  


        for row in data:
            
            self.values.append(row[1])
            self.idValues.append(row[0])

       
        self.config(values=self.values)

        self.bind("<<ComboboxSelected>>", self._get_value_id)
        self.__variable.trace_add('write', callback=lambda v,m,i: self._get_value_description())

        if self.__variable.get() > 0:
            self._get_value_description()
        else:
            self.current(0)

    def _get_value_id(self, e):
        index = self.values.index(self.get())
        self.__variable.set(self.idValues[index])

    def _get_value_description(self):
        self.delete(0, ttb.END)
        index = self.idValues.index(self.__variable.get())
        self.insert(0, self.values[index])