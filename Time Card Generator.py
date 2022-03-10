import datetime
import tkinter as tk
from tkinter import *
from tkinter import StringVar
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import *
from tkinter import filedialog
from tkcalendar import *
from ttkthemes import ThemedTk
from calendar import isleap
import os
import time
import FileWriterAndTimeCardListCreator
from Dates import Dates
from FileWriterAndTimeCardListCreator import *
from Response_Filtering import ResponseFilter

# Theme
root = ThemedTk(theme="plastik")


def main_window():
    # All the functions are at the beginning

    def calendar_date_picker(clicked_button_name: str):
        """Returns a date and puts it in the entry boxes based on the button clicked"""
        button_name = clicked_button_name
        # Window measurements and location
        calendar_height = "220"
        calendar_width = "300"
        # calendar_location = "+1110+200"
        calendar_location = "+450+250"
        calendar_window = tk.Tk()
        calendar_window.title("Select a date")
        calendar_window.geometry(
            calendar_width + "x" + calendar_height + calendar_location)
        # Ex:('700x500')
        calendar_window.resizable(0, 0)
        # Window icon location
        location = r"clock.ico"
        # Changes the Tkinter feather icon to berry it icon
        calendar_window.iconbitmap(location)
        now = datetime.datetime.now()

        def grab_date(event):
            non_formatted_date = cal.get_date()
            formatted_date = datetime.datetime.strptime(non_formatted_date, "%m/%d/%y")
            if button_name == "starting_date_calendar_button":
                starting_date_entry_box_year.delete(0, END)
                starting_date_entry_box_year.insert(0, formatted_date.year)
                starting_date_entry_box_month.delete(0, END)
                starting_date_entry_box_month.insert(0, formatted_date.month)
                starting_date_entry_box_day.delete(0, END)
                starting_date_entry_box_day.insert(0, formatted_date.day)
            elif button_name == "ending_date_calendar_button":
                ending_date_entry_box_year.delete(0, END)
                ending_date_entry_box_year.insert(0, formatted_date.year)
                ending_date_entry_box_month.delete(0, END)
                ending_date_entry_box_month.insert(0, formatted_date.month)
                ending_date_entry_box_day.delete(0, END)
                ending_date_entry_box_day.insert(0, formatted_date.day)

            # Closes the window once a date is selected
            calendar_window.destroy()

        # Calendar format
        cal = Calendar(calendar_window,
                       selectmode="day",
                       year=now.year,
                       month=now.month,
                       day=now.day)
        cal.pack(fill="both", expand=True)
        cal.bind("<<CalendarSelected>>", grab_date)

    def starting_date_calendar():
        calendar_date_picker("starting_date_calendar_button")

    def ending_date_calendar():
        calendar_date_picker("ending_date_calendar_button")

    # Manages what happens when you press the Enter key inside an entry box
    def enter_key_pressed_event_handler(event):
        if starting_date_entry_box_month.get() != '':
            starting_date_entry_box_day.focus()
            if starting_date_entry_box_day.get() != '':
                starting_date_entry_box_year.focus()
                if starting_date_entry_box_year.get() != '':
                    ending_date_entry_box_month.focus()
                    if ending_date_entry_box_month.get() != '':
                        ending_date_entry_box_day.focus()
                        if ending_date_entry_box_day.get() != '':
                            ending_date_entry_box_year.focus()
                            if ending_date_entry_box_year.get() != '':
                                generate_button.focus()
                            else:
                                ending_date_entry_box_year.focus()
                        else:
                            ending_date_entry_box_day.focus()
                    else:
                        ending_date_entry_box_month.focus()
                else:
                    starting_date_entry_box_year.focus()
            else:
                starting_date_entry_box_day.focus()
        else:
            starting_date_entry_box_month.focus()

    # Dialog window asks user for path and file name
    def file_dialog():
        today = Dates.get_date_today_string()
        file_directory = filedialog.asksaveasfilename(initialfile=f"Time_card_{today}",
                                                      filetypes=(("CSV", '.csv'), ("All Files", '*.*')),
                                                      defaultextension="*.*")
        if not file_directory:
            return 'None'
        else:
            return file_directory

    # Breaks down a path into three parts (path, filename, and extension)
    def path_parser(path_with_file_name_and_extension):
        complete_path = path_with_file_name_and_extension
        path_only = os.path.dirname(complete_path)
        file_name_with_extension = os.path.basename(complete_path)
        filename, extension = os.path.splitext(file_name_with_extension)
        return path_only, filename, extension

    # Does most of the processing and error handing
    def create_button_clicked_event_handler():
        # Gets user entries from radio buttons
        date_selection_value = date_radio_button_selection.get()
        amount_of_files_value = amount_of_files_radio_button_selection.get()
        # Initialize booleans
        date_radio_button_selected = False
        file_radio_button_selected = False
        other_error_found = False

        # Handles what happens when the single date radio button is selected
        if date_selection_value == "Single":
            date_radio_button_selected = True
            # This has to be proved otherwise
            other_error_found = True
            # Looks for month errors
            month_error_found = month_entry_box_error_handler(starting_date_value_month)
            # Looks for day errors if month errors are not found
            if not month_error_found:
                day_error_found = day_entry_box_error_handler(starting_date_value_month,
                                                              starting_date_value_day,
                                                              starting_date_value_year)
                # Looks for year errors if day errors are not found
                if not day_error_found:
                    year_error_found = year_entry_box_error_handler(starting_date_value_year)
                    # Creates the starting date string if there are no errors found
                    if not year_error_found:
                        other_error_found = False
                        # This will be used later to generate the time cards
                        starting_date_str_obj = f"{starting_date_value_year.get()}-{starting_date_value_month.get()}-{starting_date_value_day.get()}"
                        ending_date_str_obj = "None"

        # Handles what happens when the multiple date radio button is selected
        elif date_selection_value == "Range":
            date_radio_button_selected = True
            # This has to be proved otherwise
            other_error_found = True
            # Looks for month errors
            starting_month_error_found = month_entry_box_error_handler(starting_date_value_month)
            # Looks for day errors if month errors are not found
            if not starting_month_error_found:
                starting_day_error_found = day_entry_box_error_handler(starting_date_value_month,
                                                                       starting_date_value_day,
                                                                       starting_date_value_year)
                # Looks for year errors if day errors are not found
                if not starting_day_error_found:
                    starting_year_error_found = year_entry_box_error_handler(starting_date_value_year)
                    # Looks for month errors if starting year errors are not found
                    if not starting_year_error_found:
                        ending_month_error_found = month_entry_box_error_handler(ending_date_value_month)
                        # Looks for day errors if month errors are not found
                        if not ending_month_error_found:
                            ending_day_error_found = day_entry_box_error_handler(ending_date_value_month,
                                                                                 ending_date_value_day,
                                                                                 ending_date_value_year)
                            # Looks for year errors if day errors are not found
                            if not ending_day_error_found:
                                ending_year_error_found = year_entry_box_error_handler(ending_date_value_year)
                                # Creates the starting date and ending date strings if there are no errors found
                                if not ending_year_error_found:
                                    other_error_found = False
                                    # These will be used later to generate the time cards
                                    starting_date_str_obj = f"{starting_date_value_year.get()}-{starting_date_value_month.get()}-{starting_date_value_day.get()}"
                                    ending_date_str_obj = f"{ending_date_value_year.get()}-{ending_date_value_month.get()}-{ending_date_value_day.get()}"

        # Handles what happens when neither is selected
        else:
            no_date_radio_button_selected_event_handler()
            date_radio_button_selected = False
            other_error_found = True

        # Verifies that one of the file section radio buttons is selected
        if amount_of_files_value == "Single" or amount_of_files_value == "Multiple":
            file_radio_button_selected = True
        # elif amount_of_files_value == "Multiple":
        #     file_radio_button_selected = True
        elif (date_radio_button_selected is True) and (other_error_found is False) and (
                file_radio_button_selected is False):
            file_radio_button_selected = False
            messagebox.showerror(title="Error",
                                 message="Please select an option from the bottom section")
        # This is where the files get generated
        if date_radio_button_selected is True and file_radio_button_selected is True:
            # Calls the file dialog that asks for the path and file name
            file_path = file_dialog()
            # Loop runs if user doesn't select a path/filename
            while file_path == "None":
                messagebox.showerror(title="Error",
                                     message="Please select a path and file name")
                file_path = file_dialog()
            # Changes the pointer to loading mode
            loading()
            # Grabs the starting date and changes it to a string
            starting_date_str_obj = Dates().format_date_str(starting_date_str_obj)
            # DDivides the path into three parts
            path_only, file_name, extension = path_parser(file_path)
            # print(path_only, file_name, extension)
            # Creates the time card cvs if the user selected single date and single file
            if date_selection_value == "Single":
                time_card_obj = single_week_time_cards(starting_date_str_obj)
                time_card_obj_filtered = ResponseFilter.timeCardHell(time_card_obj, starting_date_str_obj)
                file_writer(f"{file_path}", time_card_obj_filtered)
            # Creates the time card cvs if the user selected date range
            elif date_selection_value == "Range":
                # Grabs the ending date and changes it to a string
                ending_date_str_obj = Dates().format_date_str(ending_date_str_obj)
                # Calls the date class and passes the starting and ending date strings
                dates_class_obj = Dates(starting_date_str_obj, ending_date_str_obj)
                # Gets the list of dates based on the starting and ending dates
                list_of_dates = dates_class_obj.get_list_of_dates()
                # Calls the method that retrieves multiple time cards from ADP in the main class
                time_card_list_obj = multiple_week_time_cards(starting_date_str_obj, ending_date_str_obj)
                # Creates a single file depending on the user selection
                if amount_of_files_value == "Single":
                    list_of_time_cards = []
                    # Loop adds all the filtered time cards to the list of time cards
                    for single_date in list_of_dates:
                        time_card_obj_filtered = ResponseFilter.timeCardHell(time_card_list_obj, str(single_date))
                        list_of_time_cards.append(time_card_obj_filtered)
                    # Creates the file
                    file_writer_multiple_days(f"{path_only}\{file_name}{extension}", list_of_time_cards)
                # Creates multiple files depending on the user selection
                elif amount_of_files_value == "Multiple":
                    # Counter
                    time_card_number = 1
                    # Loop filters all the time cards and generates a file for each date in the range given by the user
                    for single_date in list_of_dates:
                        time_card_list_obj_filtered = ResponseFilter.timeCardHell(time_card_list_obj, str(single_date))
                        file_writer(f"{path_only}/{file_name}_({time_card_number}){extension}",
                                    time_card_list_obj_filtered)
                        time_card_number += 1
            # Changes pointer back to normal
            not_loading()
            # Creates a message box
            messagebox.showinfo(title="Info",
                                message="Completed")

            # print(file_path)

    # changes the cursor to "loading"
    def loading():
        root.config(cursor='wait')

    # changes the cursor to normal
    def not_loading():
        root.config(cursor='')

    # Menu Bar Function (needs work)
    def file_radio_button_selected_event_handler():
        pass

    def close_window_event_handler():
        response = messagebox.askquestion("Close?", "Are you sure you want to close the program?")
        if response == "yes":
            global root
            root = root.destroy()

    def month_entry_box_error_handler(month_widget_name):
        value_month = month_widget_name.get()
        month_error_found = False
        # Check if the field contains only integers
        if not value_month.isdigit() or (len(value_month) == 0) or (int(value_month) <= 0) or (int(value_month) > 12):
            month_error_found = True
            messagebox.showerror(title="Error",
                                 message="Please enter a valid month")
        return month_error_found

    def day_entry_box_error_handler(month_widget_name, day_widget_name, year_widget_name):
        day_error_found = False
        value_month = month_widget_name.get()
        value_day = day_widget_name.get()
        value_year = year_widget_name.get()
        # Checks if the month is February
        if not value_day.isdigit() or (len(value_day)) == 0 or (int(value_day) <= 0) or (int(value_day) > 31):
            day_error_found = True
            messagebox.showerror(title="Error",
                                 message="Please enter a valid day")
        elif int(value_month) == 2:
            # makes sure the user does not enter a number higher than 29 for February
            # Need to fix for non-leap years
            if int(value_day) == 29:
                if not isleap(int(value_year)):
                    day_error_found = True
                    messagebox.showerror(title="Error",
                                         message="Please enter a valid day")

        return day_error_found

    def year_entry_box_error_handler(year_widget_name):
        year_error_found = False
        value_year = year_widget_name.get()
        now = datetime.datetime.now()
        if not value_year.isdigit() or (len(value_year) == 0) or (len(value_year) < 4) or len(value_year) > 4:
            year_error_found = True
            messagebox.showerror(title="Error",
                                 message="Please enter a valid year")
        elif int(value_year) <= 0 or int(value_year) > now.year + 1:
            year_error_found = True
            messagebox.showerror(title="Error",
                                 message="Please enter a valid year year")
        return year_error_found

    def no_date_radio_button_selected_event_handler(*args):
        messagebox.showerror(title="Error",
                             message="Please select one option from the top section")

    def no_file_radio_button_selected_event_handler(*args):
        messagebox.showerror(title="Error",
                             message="Please select one option from the bottom section")

    def disable_ending_date_widgets(*args):
        # Remove widgets
        ending_date_calendar_button.place_forget()
        ending_date_label.place_forget()
        ending_date_entry_box_month.place_forget()
        ending_date_entry_box_day.place_forget()
        ending_date_entry_box_year.place_forget()
        ending_date_frame.place_forget()

    def move_starting_date_widgets_to_center(*args):
        # Move widgets
        starting_date_calendar_button.place(relx=0.88, rely=0.36, relwidth=0.09, relheight=0.08)
        starting_date_label.place(relx=0, rely=0, relwidth=0.44, relheight=1)
        starting_date_entry_box_month.place(relx=0.45, rely=0, relwidth=0.14, relheight=1)
        starting_date_entry_box_day.place(relx=0.6, rely=0, relwidth=0.14, relheight=1)
        starting_date_entry_box_year.place(relx=0.75, rely=0, relwidth=0.24, relheight=1)
        starting_date_frame.place(relx=0.05, rely=0.36, relwidth=0.8, relheight=0.08)

    def move_starting_date_widgets_to_original_position(*args):
        # Move widgets
        starting_date_calendar_button.place(relx=0.88, rely=0.30, relwidth=0.09, relheight=0.08)
        starting_date_label.place(relx=0, rely=0, relwidth=0.44, relheight=1)
        starting_date_entry_box_month.place(relx=0.45, rely=0, relwidth=0.14, relheight=1)
        starting_date_entry_box_day.place(relx=0.6, rely=0, relwidth=0.14, relheight=1)
        starting_date_entry_box_year.place(relx=0.75, rely=0, relwidth=0.24, relheight=1)
        starting_date_frame.place(relx=0.05, rely=0.30, relwidth=0.8, relheight=0.08)

    def move_ending_date_widgets_to_original_position(*args):
        # Place widgets
        ending_date_calendar_button.place(relx=0.88, rely=0.42, relwidth=0.09, relheight=0.08)
        ending_date_label.place(relx=0, rely=0, relwidth=0.44, relheight=1)
        ending_date_entry_box_month.place(relx=0.45, rely=0, relwidth=0.14, relheight=1)
        ending_date_entry_box_day.place(relx=0.6, rely=0, relwidth=0.14, relheight=1)
        ending_date_entry_box_year.place(relx=0.75, rely=0, relwidth=0.24, relheight=1)
        ending_date_frame.place(relx=0.05, rely=0.42, relwidth=0.8, relheight=0.08)

    def date_radio_button_selection_event_handler(*args):
        date_selection_value = date_radio_button_selection.get()
        # Value 1 is single date and value 2 is date range
        if date_selection_value == "Single":
            starting_date_label.configure(text="Date: ")
            # Remove Widgets
            disable_ending_date_widgets()
            # Move Widgets to center
            move_starting_date_widgets_to_center()
            radio_button_multiple_files.configure(state="disabled")
        elif date_selection_value == "Range":
            starting_date_label.configure(text="Starting date:")
            # Move widgets to original position
            move_starting_date_widgets_to_original_position()
            # Place ending date widgets in original position
            move_ending_date_widgets_to_original_position()
            # Disable the multiple files radio button
            radio_button_multiple_files.configure(state="!disabled")

    # Main window size and location
    main_window_height = "350"
    main_window_width = "300"
    # main_window_location = "+700+200"
    main_window_location = "+100+200"
    # Main window name
    global root

    # window background, title, and measures
    # root.configure(bg="#D6D6D7")
    root.configure(bg="#555555")
    root.title("ADP Time Card Generator")
    root.geometry(main_window_width + "x" + main_window_height + main_window_location)  # Ex: ('700x500')
    # This disables the maximize button
    # root.resizable(0, 0)
    # Overrides the x button control
    root.protocol("WM_DELETE_WINDOW", close_window_event_handler)
    # Make window slightly transparent
    # root.attributes('-alpha', 0.9)
    root.minsize(300, 350)
    root.maxsize(400, 450)
    # Window icon location
    window_icon_location = r"clock.ico"
    # Changes the Tkinter feather icon to something else
    root.iconbitmap(window_icon_location)

    # Font type and size for all the labels, buttons, and text boxes
    # Font sizes
    font_open_sans_size_15 = ("Segoe UI", 14)
    font_open_sans_size_13 = ("Segoe UI", 12)
    # tkinter styles
    style = ttk.Style()
    # Labels style
    style.configure("my.TLabel",
                    font=font_open_sans_size_13,
                    background="#555555",
                    justify=LEFT, foreground="#FFFFFF")
    # Frames style
    style.configure("gray.TFrame",
                    background="#555555", relief=FLAT)
    # relief=GROOVE)  # RIDGE is also a good option
    style.configure("dark_gray.TFrame",
                    background="#555555",
                    relief=FLAT)
    # Buttons style
    style.configure("my.TButton",
                    font=font_open_sans_size_15, background="#474444")
    # Radio Button style ###               background="#D6D6D7",
    style.configure("my.TRadiobutton",
                    font=font_open_sans_size_13,
                    background="#555555", foreground="#FFFFFF")

    # Frames
    date_range_radio_buttons_frame = ttk.Frame(root, style="dark_gray.TFrame")

    starting_date_frame = ttk.Frame(root, style="dark_gray.TFrame")

    ending_date_frame = ttk.Frame(root, style="dark_gray.TFrame")

    multiple_files_frame = ttk.Frame(root, style="dark_gray.TFrame")

    get_hours_frame = ttk.Frame(root, style="blue.TFrame")

    # Place frames
    date_range_radio_buttons_frame.place(relx=0.02, rely=0.05, relwidth=0.9, relheight=0.2)
    starting_date_frame.place(relx=0.05, rely=0.30, relwidth=0.8, relheight=0.08)
    ending_date_frame.place(relx=0.05, rely=0.42, relwidth=0.8, relheight=0.08)
    multiple_files_frame.place(relx=0.02, rely=0.55, relwidth=0.9, relheight=0.2)
    get_hours_frame.place(relx=0.62, rely=0.8, relwidth=0.35, relheight=0.1)

    # Radio Buttons

    date_radio_button_selection = StringVar()
    amount_of_files_radio_button_selection = StringVar()
    radio_button_single_date = ttk.Radiobutton(date_range_radio_buttons_frame, text="Single date",
                                               variable=date_radio_button_selection,
                                               value="Single",
                                               command=date_radio_button_selection_event_handler,
                                               style="my.TRadiobutton")
    radio_button_date_range = ttk.Radiobutton(date_range_radio_buttons_frame, text="Date range",
                                              variable=date_radio_button_selection,
                                              value="Range",
                                              command=date_radio_button_selection_event_handler,
                                              style="my.TRadiobutton")
    radio_button_single_file = ttk.Radiobutton(multiple_files_frame, text="Single file",
                                               variable=amount_of_files_radio_button_selection,
                                               value="Single",
                                               command=file_radio_button_selected_event_handler(),
                                               style="my.TRadiobutton")
    radio_button_multiple_files = ttk.Radiobutton(multiple_files_frame, text="Multiple files",
                                                  variable=amount_of_files_radio_button_selection,
                                                  value="Multiple",
                                                  command=file_radio_button_selected_event_handler(),
                                                  style="my.TRadiobutton")

    # Place radio buttons on window
    radio_button_single_date.place(relx=0, rely=0, relwidth=0.5, relheight=0.5)
    radio_button_date_range.place(relx=0, rely=0.5, relwidth=0.5, relheight=0.5)
    radio_button_single_file.place(relx=0, rely=0, relwidth=0.5, relheight=0.5)
    radio_button_multiple_files.place(relx=0, rely=0.5, relwidth=0.5, relheight=0.5)

    # Labels
    starting_date_label = ttk.Label(starting_date_frame, text="Starting date:", style="my.TLabel")
    ending_date_label = ttk.Label(ending_date_frame, text="Ending date: ", style="my.TLabel")

    # Place labels
    starting_date_label.place(relx=0, rely=0, relwidth=0.44, relheight=1)
    ending_date_label.place(relx=0, rely=0, relwidth=0.44, relheight=1)

    # Verification variables
    starting_date_value_month = StringVar()
    starting_date_value_day = StringVar()
    starting_date_value_year = StringVar()
    ending_date_value_month = StringVar()
    ending_date_value_day = StringVar()
    ending_date_value_year = StringVar()

    # Entry boxes
    starting_date_entry_box_month = tk.Entry(starting_date_frame,
                                             font=font_open_sans_size_15,
                                             justify=CENTER,
                                             textvariable=starting_date_value_month, background="#bcbcbc", relief=FLAT)

    starting_date_entry_box_day = tk.Entry(starting_date_frame,
                                           font=font_open_sans_size_15,
                                           justify=CENTER,
                                           textvariable=starting_date_value_day, background="#bcbcbc", relief=FLAT)

    starting_date_entry_box_year = tk.Entry(starting_date_frame,
                                            font=font_open_sans_size_15,
                                            justify=CENTER,
                                            textvariable=starting_date_value_year, background="#bcbcbc", relief=FLAT)

    ending_date_entry_box_month = tk.Entry(ending_date_frame,
                                           font=font_open_sans_size_15,
                                           justify=CENTER,
                                           textvariable=ending_date_value_month, background="#bcbcbc", relief=FLAT)

    ending_date_entry_box_day = tk.Entry(ending_date_frame,
                                         font=font_open_sans_size_15,
                                         justify=CENTER,
                                         textvariable=ending_date_value_day, background="#bcbcbc", relief=FLAT)

    ending_date_entry_box_year = tk.Entry(ending_date_frame,
                                          font=font_open_sans_size_15,
                                          justify=CENTER,
                                          textvariable=ending_date_value_year, background="#bcbcbc", relief=FLAT)
    # Place entry boxes
    starting_date_entry_box_month.place(relx=0.45, rely=0, relwidth=0.14, relheight=1)
    starting_date_entry_box_day.place(relx=0.6, rely=0, relwidth=0.14, relheight=1)
    starting_date_entry_box_year.place(relx=0.75, rely=0, relwidth=0.24, relheight=1)
    ending_date_entry_box_month.place(relx=0.45, rely=0, relwidth=0.14, relheight=1)
    ending_date_entry_box_day.place(relx=0.6, rely=0, relwidth=0.14, relheight=1)
    ending_date_entry_box_year.place(relx=0.75, rely=0, relwidth=0.24, relheight=1)

    # Bind entry boxes
    # Focuses on the next entry box only enter is presses
    starting_date_entry_box_month.bind("<Return>", enter_key_pressed_event_handler)
    starting_date_entry_box_day.bind("<Return>", enter_key_pressed_event_handler)
    starting_date_entry_box_year.bind("<Return>", enter_key_pressed_event_handler)
    ending_date_entry_box_month.bind("<Return>", enter_key_pressed_event_handler)
    ending_date_entry_box_day.bind("<Return>", enter_key_pressed_event_handler)
    ending_date_entry_box_year.bind("<Return>", enter_key_pressed_event_handler)

    # Icons
    calendar_image = PhotoImage(file=r"cal.png")
    # photo = PhotoImage(file = r"path")
    calendar_image_formatted = calendar_image.subsample(3, 3)

    # Buttons
    generate_button = ttk.Button(get_hours_frame,
                                 text="Create",
                                 style="my.TButton",
                                 command=create_button_clicked_event_handler)

    starting_date_calendar_button = ttk.Button(root,
                                               image=calendar_image_formatted,
                                               style="my.TButton",
                                               command=starting_date_calendar)
    ending_date_calendar_button = ttk.Button(root,
                                             image=calendar_image_formatted,
                                             style="my.TButton",
                                             command=ending_date_calendar)

    # Place buttons
    generate_button.place(relx=0, rely=0, relwidth=1, relheight=1)
    starting_date_calendar_button.place(relx=0.88, rely=0.30, relwidth=0.085, relheight=0.08)
    ending_date_calendar_button.place(relx=0.88, rely=0.42, relwidth=0.085, relheight=0.08)

    root.mainloop()


main_window()
