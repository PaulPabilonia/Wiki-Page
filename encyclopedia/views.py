from django.shortcuts import render

from . import util
import markdown
# i use markdown instead of markdown2 for simplicity
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#function that convert markdown to hmtl
def convert_to_html(title):
    #first get the entry using the title parameter
    entry = util.get_entry(title)
    #then convert the markdown to html if the entry exist else return none
    html = markdown.markdown(entry) if entry else None
    return html

def entry(request,title):
    #gets the entry to the util using the title parameter
    entryPage = util.get_entry(title)
    #checks wether the page exist or not
    if entryPage is None:
        #if page does not exist it will return to pageDoesNotExist page including the title
        return render(request, "encyclopedia/pageDoesNotExist.html",{
            "entryTitle":title
        })
    else:
        #if page does exist it will return the page ,title and convert it to html
       return render(request, "encyclopedia/entry.html", {
			"entry": convert_to_html(title),
			"entryTitle": title
			}) 

def editPage(request):
    #fuction that let you edit the content of the page
	if request.method == 'POST': #using POST because we are changing/edit something
        #we take the title name using the "name" attribute in the input form
		input_title = request.POST['title']
        #it will get the existing entrypage using the util.get_entry
		text = util.get_entry(input_title)

		return render(request, "encyclopedia/editPage.html",{
			"entry": text, #this will take the value of the page to edit the content value
			"entryTitle": input_title #this is the title of the page.
		})

def saveEdit(request):
    """ 
    This function saves the changes in the edit Page
    Basically this is the fuction of the save input button in the edit page
    """
    if request.method == 'POST':
        """
        First it will check if the form is using POST since
        we are changing the content of the Page.
        """
        #We will get the title and content first to edit it.
        entryTitle = request.POST['title'] 
        entry = request.POST['content']
        #we will save the changes using util.save_entry
        util.save_entry(entryTitle,entry)
        html = convert_to_html(entryTitle)
        #then it will return the save changes
        return render(request, "encyclopedia/entry.html",{
            'entry': html,
            "entryTitle": entryTitle
        })

def randomPage(request):
    #First retrive all the entries using util.list_entries
    entries = util.list_entries()
    #using random.choice it will pick one entry randomly from the existing entries
    randomEntry = random.choice(entries)
    #then it will convert the markdown to html
    html = convert_to_html(randomEntry)
    #this will render the page with the title and content
    return render(request,'encyclopedia/entry.html',{
        'entry': html,
        'entryTitle': randomEntry
    })

def newPage(request):
    #this will render the newPage page form
    return render(request,"encyclopedia/newPage.html")

def saveNewPage(request):
    #this save the content and title of the new page that we create
    if request.method == 'POST':
        """
        First it will check if the form is using POST method 
        We are using POST because we are changing the state of the system
        then it will retrive that value of the 'title' and 'content' of the form
        using the name attribute of the input
        """
        input_title = request.POST['title']
        input_content = request.POST['content']
        #This will retreive the list of all entry
        entries = util.list_entries()
        """
        First we need to assume that the page that we are
        trying to create is NOT existing in the 'entries' list/file
        """
        entry_exist = False
        for entry in entries:
            """
            this will iterate to the existing entries
            and compare the title that we trying to create to the existing entry list
            if the Title is equal to an exisiting entry then
            we can say that entry_exist is TRUE
            """
            if input_title.upper().strip() == entry.upper().strip():
                entry_exist = True
        
        if entry_exist == True:
            """
            If the entry that we are trying to create is already exist then
            It will render that existing entry instead of creating a new page.
            """
            return render(request,"encyclopedia/entryExist.html",{
                "entry":convert_to_html(input_title),
                "entryTitle": input_title
            })
        else:
            """
            this will exceute if the entry that we are trying to create doesn't exist
            using the save_entry it will save the title and content of our page
            then it will render the page that we created.
            """
            util.save_entry(input_title,input_content)
            return render(request,"encyclopedia/entry.html",{
                "entry": convert_to_html(input_title),
                "entryTitle": input_title
            })

def search(request):
    """
    This function renders the page that we try to search using 
    the input text(search bar) 
    in a form from the layout.html
    """
    if request.method == 'GET':
        #we are using GET since we are only retrieving pages and not changing the content
        #input(value of the searchbar) we use .get to retrive the value
        input = request.GET.get('q')
        html = convert_to_html(input)
        #this is used for later for comparison of the input and entries
        entries = util.list_entries()

        #we declared a list outside the for loop so that we can append all the list after each iteration
        search_pages = []
        for entry in entries:
            if input.upper() in entry.upper():
                """
                This will check for similarities in spelling
                eg. For example, if the search query were 'ytho', 
                then 'Python' should appear in the search results.

                we append all the page that has similar spelling
                to render them all later.
                """
                search_pages.append(entry)

        for entry in entries:
            """
            this loop compare that input in search bar to an existing entry in the entries list
            """
            if input.upper() == entry.upper():
                """
                if the input is equal to an exisiting entry
                then it will render that entry page
                """
                return render(request, "encyclopedia/entry.html",{
                    "entry": html,
					"entryTitle": input
				})
            elif search_pages != "":
                """
                if the search_pages list is not empty then
                it will render all the similar pages using the 
                entry/entries that we append
                """
                return render(request, "encyclopedia/search.html",{
					"entries": search_pages
					})
            else:
                """
                if the page does not exist it will render the
                page does not exist page using the value of the input. 
                For example, _______(value of you are trying to search) does not exist!.
                """
                return render(request, "encyclopedia/pageDoesNotExist.html",{
					"entryTitle": input 
					})

