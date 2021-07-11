from imports import *

def gui():
    try:
        jvm.start(packages=True, system_cp=True,)

        gui.window = Tk() 
        gui.window.title("Welcome to Weka J48 App")
        w,h = 800,600
        ws = gui.window.winfo_screenwidth()
        hs = gui.window.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        gui.window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        options = [
            "Load Data File",
            "PreProcess Data",
            "Load CSV File",
            "Convert CSV to Arff",
            "Load Arff File",
            "Classify",
            "Show CSV",
            "Visualize",
        ]

        gui.clicked = StringVar()
        gui.clicked.set("OPTIONS: ")
        btn1 = Button(gui.window, text='CLICK FOR HELP', command=button_help)
        btn1.pack(side=BOTTOM,fill=X)
        dropDown = OptionMenu(gui.window, gui.clicked, *options, command=selected)
        dropDown.place(x=0,y=200)
        dropDown.pack(fill=X)
        labelInfo = Label(gui.window, text="Classify options: ")
        labelInfo.pack(ipadx=1, ipady=1)
        gui.textbox = Text(gui.window, height=1, width=35)
        gui.textbox.pack()
        gui.window.mainloop()
    except Exception as e:
        print(traceback.format_exc())
    finally:
        jvm.stop()

def button_help():
    a = """
           1. Load Data File
           2. PreProcess data, it will be saved as CSV
           3. Load CSV
           4. Convert CSV to Arff
           5. Load Arff file
           5. Classify with or without parameteres.

           Use Show CSV to display an data in table.
           Use Visualization button for visualization
        
“-U” Use unpruned tree.
“-O” Do not collapse tree.
“-C <pruning confidence>” Set confidence threshold for pruning.
“-M <minimum number of instances>” Set minimum number of instances per leaf.
“-R” Use reduced error pruning.
“-N” <> Set number of folds for reduced error pruning. One fold is used as pruning set.
 “-B” Use binary splits only.
“-S” Don't perform subtree raising.
“-L” Do not clean up after the tree has been built.
“-A” Laplace smoothing for predicted probabilities.
“-J” Do not use MDL correction for info gain on numeric attributes. 
“-Q <seed>” Seed for random data shuffling.
“-doNotMakeSplitPointActualValue” Do not make split point actual value.
"""
    return msg.showinfo(' INSTRUCTIONS ', a)

def show_csv():
    try:
        xlsName = ("test3.xls")
        fileName = fd.askopenfilename(title = 'Select a CSV file',filetypes = (('csv file','*.csv'), ('csv file','*.csv')))
        if os.path.isfile(fileName):
            msg.showinfo('ATTENTION', 'CSV file loaded')
        else:
            msg.showerror('Error', 'Cannot load CSV file')
        readCsv = pd.read_csv(fileName)
        with pd.ExcelWriter(xlsName) as writer:
                            readCsv.to_excel(writer)
                            writer.save()
                            msg.showinfo('ATTENTION', 'Excel file created')  
        msg.showinfo('ATTENTION', 'XLS file loaded')
        xlsData = pd.read_excel(xlsName)
        xlsData = xlsData[xlsData.filter(regex='^(?!Unnamed)').columns]
        f2 = Frame(gui.window, height=200, width=300)
        f2.pack(side=BOTTOM,ipady=300,expand=1)
        table = Table(f2, dataframe=xlsData,read_only=True, editable=False)
        table.show()
        msg.showinfo('ATTENTION', 'Done')
    except Exception as e:
        msg.showerror('Error', e)
#endregion

def retrieve_input():
    retrieve_input.inputValue = gui.textbox.get("1.0","end-1c")
    return retrieve_input.inputValue

def selected(event):
    if gui.clicked.get() == "PreProcess Data":
        return pre_process()
    if gui.clicked.get() == "Load CSV File":
        return load_csv_file(csvFileName=fd.askopenfilename(filetypes=[("CSV data files","*.CSV")]))
    if gui.clicked.get() == "Convert CSV to Arff":
        return save_csv_as_arff()
    if gui.clicked.get() == "Load Arff File":
        return load_arff_file(arffFileName=fd.askopenfilename(filetypes=[("Arff data files","*.arff")]))
    if gui.clicked.get() == "Classify":
        return weka()
    if gui.clicked.get() == "Show CSV":
        return show_csv()
    if gui.clicked.get() == "Visualize":
        return visualization()
    if gui.clicked.get() == "Load Data File":
        return load_data_file()

def load_data_file():
    try:
       load_data_file.dataFileName = fd.askopenfilename(title = 'Select a data file',filetypes = (('data file','*.data'), ('data file','*.data')))
       if os.path.isfile(load_data_file.dataFileName):
            msg.showinfo('ATTENTION', 'Data file loaded')
       else:
           msg.showerror('Error', 'Cannot load Data file')  
    except Exception as e:
       msg.showerror('Error', e)


def load_arff_file(arffFileName):
    try:
        loader = Loader("weka.core.converters.ArffLoader")
        load_arff_file.loadedArffFile = loader.load_file(arffFileName)
        if load_arff_file.loadedArffFile is not None:
            msg.showinfo('ATTENTION', 'Arff file loaded')
        else:
            msg.showerror('Error', 'Cannot load Arff file')
    except Exception as e:
        msg.showerror('Error', e)

def load_csv_file(csvFileName):
    try:
        loader = Loader(classname="weka.core.converters.CSVLoader")
        load_csv_file.loadedCsvFile = loader.load_file(csvFileName)
        if load_csv_file.loadedCsvFile is not None:
            msg.showinfo('ATTENTION', 'CSV file loaded')
        else:
            msg.showerror('Error', 'Cannot load CSV file')
    except Exception as e:
        msg.showerror('Error', e)

def save_csv_as_arff():
    try:
        loader = Saver(classname="weka.core.converters.ArffSaver")
        outfile = ("test3.arff")
        data = load_csv_file.loadedCsvFile
        save_csv_as_arff.arff = loader.save_file(data, outfile)
        msg.showinfo('ATTENTION', 'CSV converted to ArFF')
    except Exception as e:
        msg.showerror('Error', e)

#region weka #classify
def weka():
    try:  
        retrieve_input()
        data = load_arff_file.loadedArffFile
        data.class_is_last()
        options1 = split_options(retrieve_input.inputValue)
        weka.classifier = Classifier(classname="weka.classifiers.trees.J48", options=options1)
        evaluation = Evaluation(data)
        evaluation.crossvalidate_model(weka.classifier, data, 10, Random(0))
        weka.classifier.build_classifier(data)
        print(evaluation.summary())
        print(weka.classifier)
        evaluation_window(evaluation)
    except Exception as e:
        msg.showerror('Error', e)

def evaluation_window(evaluation):
    newWindow = Toplevel(gui.window)
    newWindow.title('evaClass')
    w,h = 600, 900
    ws = gui.window.winfo_screenwidth()
    hs = gui.window.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    newWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))
    Label(newWindow, text="////// Evaluation summary //////  \n").pack(side=TOP)
    Label(newWindow, text=evaluation.summary()).pack(side=TOP)
    Label(newWindow, text=" //////  Classifier //////  \n").pack(side=TOP)  
    Label(newWindow, text=weka.classifier).pack(side=TOP)
    Label(newWindow, text="//////  Evaluation Matrix ////// \n").pack(side=TOP)
    Label(newWindow, text=evaluation.matrix()).pack(side=TOP)
    Label(newWindow, text="////// Evaluation class ////// \n").pack(side=TOP)
    Label(newWindow, text=evaluation.class_details()).pack(side=TOP)
    Button(newWindow, text="CLOSE", command=lambda: newWindow.destroy()).pack(side=BOTTOM,fill=X,ipady=50)
#endregion

def visualization():
    try:
        retrieve_input()
        data = load_arff_file.loadedArffFile
        data.class_is_last()
        options1 = split_options(retrieve_input.inputValue)
        weka.classifier = Classifier(classname="weka.classifiers.trees.J48", options=options1)
        weka.classifier.build_classifier(data)
        graph.plot_dot_graph(weka.classifier.graph, 'DOTgraph.png')
        cls = [
        Classifier(classname="weka.classifiers.trees.J48"),
        Classifier(classname="weka.classifiers.bayes.NaiveBayesUpdateable")]
        plot_cls.plot_learning_curve(cls, data, increments=0.05, label_template="[#] !", metric="percent_correct", wait=True)
    except:
        msg.showerror("Error","Load arff file")
        
def pre_process():
    try:
        A.each_line_to_array(file=load_data_file.dataFileName)
        A.each_line_to_array_dec(file=load_data_file.dataFileName)
        A.maths()
        msg.showinfo('ATTENTION', 'PreProcessing is done')
    except Exception as e:
        msg.showerror('Error', e)
       
gui()