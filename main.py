from window.GUI import Main



if __name__=="__main__":
    try:
        app = Main(themename='new')   
        app.mainloop()
    except:
        app.quit()


