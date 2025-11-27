from ttkbootstrap import Style
from assets.globals import GUI_COLORS, GUI_FONT

class SGDB_Style:
    def __init__(self):
        self.GUIstyle = Style()

        self.GUIstyle.configure('flat.primary.TButton',focuscolor='#B4B4B4', background='#B4B4B4', darkcolor='#B4B4B4', lightcolor='#B4B4B4', border=0, bordercolor='#B4B4B4')

        self.GUIstyle.map('flat.primary.TButton', 
                    bordercolor= [
                        ('pressed !disabled', '#B4B4B4'),
                        ('hover !disabled', '#B4B4B4'),
                        ('disabled', GUI_COLORS['light'])
                    ],
                    darkcolor = [
                        ('hover !disabled', '#B4B4B4'),
                    ],
                    lightcolor = [ ('hover !disabled', '#B4B4B4'),],
                    background=[
                        ('disabled', GUI_COLORS['light']),
                        ('hover !disabled', '#B4B4B4'),
                    ]
                )

        self.GUIstyle.configure('TButton', 
                            font=(GUI_FONT,10, 'bold'), anchor='w'
                            )

        self.GUIstyle.configure('dark.Treeview', 
                                    rowheight=40,
                                    font=('arial',10))
                
        self.GUIstyle.configure('aside.TButton', 
                                    font=(GUI_FONT,11, 'bold'), focuscolor=GUI_COLORS['primary'])
                
        self.GUIstyle.configure('asideselected.TButton',font=(GUI_FONT,11, 'bold'),foreground='#fff', focuscolor='#EF8B47',
                                        background='#EF8B47', bordercolor='#EF8B47', darkcolor='#EF8B47', lightcolor='#EF8B47')
                

        self.GUIstyle.map('asideselected.TButton', 
                    bordercolor= [
                        ('pressed !disabled', '#EF8B47'),
                        ('hover !disabled', '#EF8B47'),
                        ('disabled', '#EF8B47')
                    ],
                    lightcolor=[
                        ('disabled', '#EF8B47')
                    ],
                    darkcolor=[
                        ('disabled', '#EF8B47')
                    ],
                    background=[
                        ('disabled', '#EF8B47'),
                        ('active !disabled', '#EF8B47'),
                        ('pressed !disabled', '#EF8B47'),
                        ('selected !disabled', '#EF8B47'),
                        ('hover !disabled', '#EF8B47'),
                    ]
                )
                
        self.GUIstyle.configure('search.TEntry', 
                                    background=GUI_COLORS['primary'],
                                    highlightcolor='red', 
                                    highlightbackground='red',
                                    border=0)
                
                #self.GUIstyle.configure('light.TButton',
                #                         relief='flat', 
                #                         background=GUI_COLORS['bg'],
                #                         font=('arial',10,'bold'),
                #                         padding='1 2', 
                #                         border=0, 
                #                         darkcolor=GUI_COLORS['bg'], 
                #                         lightcolor=GUI_COLORS['bg'])
                    
                    ##############SELECTION COMBOBOX STYLE ###############
        self.GUIstyle.configure('selectionOnly.TCombobox', 
                                padding=11, 
                                selectbackground='#D3D6DF', 
                                background='#D3D6DF',
                                selectforeground=GUI_COLORS['dark'],
                                foreground=GUI_COLORS['dark'],
                                )

        self.GUIstyle.map('selectionOnly.TCombobox', 
                    arrowcolor=[
                        ('disabled', 'gray'),
                    
                    ],
                    foreground = [
                        ('disabled', GUI_COLORS['dark'])
                    ],
                    selectforeground = [
                         ('disabled', GUI_COLORS['dark'])
                    ],
                    fieldbackground= [
                        ('readonly', '#D3D6DF'),
                        ('disabled', '#D3D6DF')
                    ],
                    background=[
                        ('disabled', '#D3D6DF'),
                        ('readonly', '#D3D6DF')
                    ],
                    darkcolor = [
                         ('disabled', '#D3D6DF'),
                        ('readonly', '#D3D6DF')
                    ],
                    lightcolor= [
                         ('disabled', '#D3D6DF'),
                        ('readonly', '#D3D6DF')
                    ])
                
        self.GUIstyle.configure('custom.primary.TSeparator', background='#B9B4C7')

        self.GUIstyle.configure('info.TEntry')

        self.GUIstyle.map('info.TEntry', 
                    fieldbackground=[
                        ('disabled', GUI_COLORS['light']),
                        ('readonly', GUI_COLORS['light'])
                    ], 
                    foreground =[
                        ('disabled', 'grey')
                    ],
                    background=[
                        ('disabled', GUI_COLORS['light'])
                    ],
                )

                
                ################ Icon Buttons ####################

        self.GUIstyle.configure('icon.light.TButton', 
                                    font=(GUI_FONT,10),
                                    foreground='#222A35',
                                    background=GUI_COLORS['light'],
                                    darkcolor=GUI_COLORS['light'],
                                    lightcolor=GUI_COLORS['light'],
                                    bordercolor=GUI_COLORS['light'],
                                    borderwidth=2)

        self.GUIstyle.map('icon.light.TButton', 
                    bordercolor= [
                        ('pressed !disabled', '#4A55A2'),
                        ('hover !disabled', '#4A55A2'),
                        ('disabled', GUI_COLORS['light'])
                    ],
                    lightcolor=[
                        ('disabled', GUI_COLORS['light'])
                    ],
                    darkcolor=[
                        ('disabled', GUI_COLORS['light'])
                    ],
                    background=[
                        ('disabled', GUI_COLORS['light']),
                        ('active !disabled', '#C5DFF8'),
                        ('pressed !disabled', '#C5DFF8'),
                        ('selected !disabled', '#C5DFF8'),
                        ('hover !disabled', '#C5DFF8'),
                    ]
                )

        self.GUIstyle.configure('CUSTOM.light.TButton', 
                                    font=(GUI_FONT,10),
                                    foreground='#222A35',
                                    background=GUI_COLORS['bg'],
                                    darkcolor=GUI_COLORS['bg'],
                                    lightcolor=GUI_COLORS['bg'],
                                    bordercolor=GUI_COLORS['bg'],
                                    borderwidth=2)
                
        self.GUIstyle.map('CUSTOM.light.TButton', 
                    bordercolor= [
                        ('pressed !disabled', '#4A55A2'),
                        ('hover !disabled', '#4A55A2'),
                        ('disabled', GUI_COLORS['bg'])
                    ],
                    lightcolor=[
                        ('disabled', GUI_COLORS['bg'])
                    ],
                    darkcolor=[
                        ('disabled', GUI_COLORS['bg'])
                    ],
                    background=[
                        ('disabled', GUI_COLORS['bg']),
                        ('active !disabled', '#C5DFF8'),
                        ('pressed !disabled', '#C5DFF8'),
                        ('selected !disabled', '#C5DFF8'),
                        ('hover !disabled', '#C5DFF8'),
                    ]
                )


        self.GUIstyle.configure('icon.primary.TButton', 
                                    font=(GUI_FONT,10),
                                    foreground='#222A35',
                                    background=GUI_COLORS['primary'],
                                    darkcolor=GUI_COLORS['primary'],
                                    lightcolor=GUI_COLORS['primary'],
                                    bordercolor=GUI_COLORS['primary'],
                                    borderwidth=2)

        self.GUIstyle.map('icon.primary.TButton', 
                    bordercolor= [
                        ('pressed !disabled', '#4A55A2'),
                        ('hover !disabled', '#4A55A2')
                    ],
                    background=[
                        ('disabled', 'gray'),
                        ('active !disabled', '#C5DFF8'),
                        ('pressed !disabled', '#C5DFF8'),
                        ('selected !disabled', '#C5DFF8'),
                        ('hover !disabled', '#C5DFF8'),
                    ]
                )
        
        self.GUIstyle.configure('flat.light.TButton', lightcolor=GUI_COLORS['bg'], darkcolor=GUI_COLORS['bg'], background=GUI_COLORS['bg'],foreground='#fff', font=(GUI_FONT,12,'bold'),
                        bordercolor=GUI_COLORS['bg'], focuscolor=GUI_COLORS['bg'])

        self.GUIstyle.map('flat.light.TButton', 
            bordercolor= [
                ('pressed !disabled', GUI_COLORS['bg']),
                ('hover !disabled', GUI_COLORS['bg']),
                ('disabled', GUI_COLORS['light'])
            ],
            darkcolor = [
                 ('hover !disabled', GUI_COLORS['bg']),
            ],
            lightcolor = [ ('hover !disabled', GUI_COLORS['bg']),],
            background=[
                ('disabled', GUI_COLORS['light']),
                
                ('hover !disabled', GUI_COLORS['bg']),
            ]
        )


        self.GUIstyle.configure('flatw.light.TButton', lightcolor='#fff', darkcolor='#fff', background='#fff',foreground='#fff',font=(GUI_FONT,11,'bold'),
                        bordercolor='#fff', focuscolor='#fff')

        self.GUIstyle.map('flatw.light.TButton', 
            bordercolor= [
                ('pressed !disabled', '#fff'),
                ('hover !disabled', '#fff'),
                ('disabled', '#fff')
            ],
            darkcolor = [
                 ('disabled', '#fff'),
                 ('hover !disabled', '#fff'),
            ],
            lightcolor = [  ('disabled', '#fff'),('hover !disabled', '#fff'),],
            background=[
                ('disabled', '#fff'),
                
                ('hover !disabled', '#fff'),
            ]
        )


        self.GUIstyle.configure('flatww.light.TButton', lightcolor='#fff', darkcolor='#fff', background='#fff',foreground='black',font=(GUI_FONT,10),
                        bordercolor='#fff', focuscolor='#fff')

        self.GUIstyle.map('flatww.light.TButton', 
            bordercolor= [
                ('pressed !disabled', '#fff'),
                ('hover !disabled', '#fff'),
                ('disabled', '#fff')
            ],
            darkcolor = [
                 ('disabled', '#fff'),
                 ('hover !disabled', '#fff'),
            ],
            lightcolor = [  ('disabled', '#fff'),('hover !disabled', '#fff'),],
            background=[
                ('disabled', '#fff'),
                
                ('hover !disabled', '#fff'),
            ]
        )



        self.GUIstyle.configure('white.TButton', lightcolor='#fff', darkcolor='#fff', background='#fff',foreground=GUI_COLORS['dark'],font=(GUI_FONT,11,'bold'),
                        bordercolor='#fff', focuscolor='#fff')

        self.GUIstyle.map('white.TButton', 
            bordercolor= [
                ('pressed !disabled', '#fff'),
                ('hover !disabled', '#fff'),
                ('disabled', '#fff')
            ],
            darkcolor = [
                 ('disabled', '#fff'),
                 ('hover !disabled', '#fff'),
            ],
            lightcolor = [  ('disabled', '#fff'),('hover !disabled', '#fff'),],
            background=[
                ('disabled', '#fff'),
                
                ('hover !disabled', '#fff'),
            ]
        )


        ####### FORM STYLES ########
        self.GUIstyle.configure('formsize.primary.TCombobox', padding=12, selectbackground='#D3D6DF', 
                                selectforeground=GUI_COLORS['primary'],)
        



        self.GUIstyle.configure('212946.TEntry',  background='#212946',bordercolor=GUI_COLORS['danger'], )

        self.GUIstyle.map('212946.TEntry', 
                    bordercolor= [
                        ('pressed !disabled', '#212946'),
                        ('hover !disabled', GUI_COLORS['danger']),
                        ('disabled', GUI_COLORS['danger'])
                    ],

                    lightcolor=[
                        ('disabled', '#B2B2B2')
                    ],
                    darkcolor=[
                        ('disabled', '#B2B2B2')
                    ],
                     fieldbackground=[
                        ('disabled', '#B2B2B2'),
                       
                    ],
                    background =[
                        ('disabled', '#212946')
                    ])
        #E95849

        self.GUIstyle.configure('E95849.TButton', 
                                    font=(GUI_FONT,10),
                                    foreground='#222A35',
                                    background='#E95849',
                                    darkcolor='#E95849',
                                    lightcolor='#E95849',
                                    bordercolor='#E95849',
                                    focuscolor='#E95849',
                                    borderwidth=2)

        self.GUIstyle.map('E95849.TButton', 
                    bordercolor= [
                        ('pressed !disabled', '#E95849'),
                        ('hover !disabled', '#E95849'),
                        ('disabled', '#E95849')
                    ],
                    lightcolor=[
                        ('disabled', '#E95849')
                    ],
                    darkcolor=[
                        ('disabled', '#E95849')
                    ],
                    background=[
                        ('disabled', '#E95849'),
                        ('active !disabled', '#E95849'),
                        ('pressed !disabled', '#E95849'),
                        ('selected !disabled', '#E95849'),
                        ('hover !disabled', '#E95849'),
                    ]
                )


        self.GUIstyle.configure('212946.TButton', 
                                    font=(GUI_FONT,11,'bold'), foreground='#fff',
                                    background='#212946',
                                    darkcolor='#212946',
                                    lightcolor='#212946',
                                    bordercolor='#212946',
                                    focuscolor='#212946',
                                    borderwidth=2)

        self.GUIstyle.map('212946.TButton', 
                    bordercolor= [
                        ('pressed !disabled', '#212946'),
                        ('hover !disabled', '#212946'),
                        ('disabled', '#212946')
                    ],
                    lightcolor=[
                        ('disabled', '#212946')
                    ],
                    darkcolor=[
                        ('disabled', '#212946')
                    ],
                    background=[
                        ('disabled', '#212946'),
                        ('active !disabled', '#212946'),
                        ('pressed !disabled', '#212946'),
                        ('selected !disabled', '#212946'),
                        ('hover !disabled', '#212946'),
                    ]
                )
        
        self.GUIstyle.configure('sad.TButton', 
                                    font=(GUI_FONT,10),
                                    foreground='#fff',
                                    background='#212946',
                                    darkcolor='#212946',
                                    lightcolor='#212946',
                                    bordercolor='#212946',
                                    focuscolor='#212946',
                                    borderwidth=2)

        self.GUIstyle.map('sad.TButton', 
                    bordercolor= [
                        ('pressed !disabled', '#212946'),
                        ('hover !disabled', '#4472C4'),
                        ('disabled', '#212946')
                    ],
                    lightcolor=[
                        ('hover !disabled', '#4472C4'),
                        ('disabled', '#212946')
                    ],
                    darkcolor=[
                        ('hover !disabled', '#4472C4'),
                        ('disabled', '#212946')
                    ],
                    background=[
                        ('disabled', '#212946'),
                        ('active !disabled', '#9BAECE'),
                        ('pressed !disabled', '#9BAECE'),
                        ('selected !disabled', '#9BAECE'),
                        ('hover !disabled', '#9BAECE'),
                    ]
                )
    

        #D6DCE5

        self.GUIstyle.configure('878C93.TFrame',  background='#878C93')


        self.GUIstyle.configure('#D9D9D9.TButton', lightcolor='#D9D9D9', darkcolor='#D9D9D9', background='#D9D9D9',
                        bordercolor='#D9D9D9', focuscolor='#D9D9D9')
        
        self.GUIstyle.map('#D9D9D9.TButton', 
            bordercolor= [
                ('pressed !disabled', '#D9D9D9'),
                ('hover !disabled', '#D9D9D9'),
                ('disabled', GUI_COLORS['light'])
            ],
            darkcolor = [
                 ('hover !disabled', '#D9D9D9'),
            ],
            lightcolor = [ ('hover !disabled', '#D9D9D9'),],
            background=[
                ('disabled', '#D9D9D9'),
                
                ('hover !disabled', '#D9D9D9'),
            ]
        )

        self.GUIstyle.configure('cust.dark.Treeview', lightcolor='#D9D9D9',darkcolor='#D9D9D9',background='#D9D9D9', relief='raised',borderwidth=3, bordercolor='#fff')

        self.GUIstyle.configure('cust.dark.Treeview.Heading', background='#fff', font=(GUI_FONT,11,'bold'), foreground=GUI_COLORS['primary'])
       
        self.GUIstyle.configure('cust.dark.Treeview.Item',padding='6 5', font=(GUI_FONT,11,'bold'), foreground=GUI_COLORS['primary'])


        self.GUIstyle.configure('white.TFrame', background='#fff')
        self.GUIstyle.configure('warning.Outline.Toolbutton', font=(GUI_FONT,10,'bold'))
        self.GUIstyle.configure('primary.Outline.Toolbutton', font=(GUI_FONT,10,'bold'))


        self.GUIstyle.configure('custom.success.TCheckbutton', background='#fff')


        self.GUIstyle.configure('list.TCombobox', padding='5 12')

        self.GUIstyle.configure('primary.TNotebook',background='#fff')

        self.GUIstyle.configure('cust.TNotebook.Tab',background='#fff')



        self.GUIstyle.configure('cust.primary.Treeview', rowheight=30, font=(GUI_FONT,10), background='#fff')

        self.GUIstyle.configure('cust.primary.Treeview.Cell', padding=4)

        self.GUIstyle.configure('cust.primary.Treeview.Heading', font=(GUI_FONT,11,'bold'))

        self.GUIstyle.configure('white.TMenubutton', background='#fff',darkcolor='#fff',light='#fff',borderwidth=0, arrowcolor=GUI_COLORS['dark'])



        self.GUIstyle.map('white.TMenubutton', 
            bordercolor= [
                ('pressed !disabled', '#fff'),
                ('hover !disabled', GUI_COLORS['light']),
                ('disabled', GUI_COLORS['light'])
            ],
             arrowcolor = [
                 ('disabled', '#fff'),
                ('active !disabled',  GUI_COLORS['warning']),
                ('pressed !disabled',  GUI_COLORS['warning']),
                ('selected !disabled',  GUI_COLORS['warning']),
                ('hover !disabled', GUI_COLORS['warning']),],
            darkcolor = [
                 ('disabled', '#fff'),
                ('active !disabled', '#fff'),
                ('pressed !disabled', '#fff'),
                ('selected !disabled', '#fff'),
                ('hover !disabled', GUI_COLORS['light']),
            ],
            lightcolor = [
                ('disabled', '#fff'),
                ('active !disabled', '#fff'),
                ('pressed !disabled', '#fff'),
                ('selected !disabled', '#fff'),
                ('hover !disabled', GUI_COLORS['light']),
            ],
            background=[
                ('disabled', '#fff'),
                ('active !disabled', '#F2F2F2'),
                ('pressed !disabled', GUI_COLORS['light']),
                ('selected !disabled', '#F2F2F2'),
                ('hover !disabled', '#F2F2F2'),
            ]
        )

