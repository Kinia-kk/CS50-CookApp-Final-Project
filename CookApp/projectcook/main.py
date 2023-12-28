import os
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, OneLineListItem, OneLineAvatarIconListItem, ILeftBody, OneLineRightIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.properties import StringProperty
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivymd.uix.imagelist import MDSmartTile
from kivymd.uix.relativelayout import RelativeLayout
from kivymd.uix.boxlayout import BoxLayout
from android.permissions import request_permissions, Permission
request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
from jnius import autoclass
Environment = autoclass('android.os.Environment')
pat= Environment.getExternalStorageDirectory().getAbsolutePath()
from database import Database
db = Database()

from kivy_window import Builder_string
from kivy.core.window import Window
Window.keyboard_anim_args = {'d':.2,'t':'in_out_expo'}
Window.softinput_mode = "below_target"

class StartScreen(Screen):
    pass
class SearchScreen(Screen):
    pass
class RecipeScreen(Screen):
    pass
class SavedRecipeScreen(Screen):
    pass
class ListScreen(Screen):
    pass

class Content(MDBoxLayout):
   pass

class ListItemWitchCheckbox(OneLineAvatarIconListItem):
    def __init__(self, pk, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    def mark(self, check, list_item):
        if check.active == True:
            db.check_shopping_completed(list_item.pk)
        else:
            db.check_shopping_incompleted(list_item.pk)

    def delete_item(self, list_item):
        name = db.delete_item(list_item.pk)
        app.shopping_list.remove(name[0][0])
        self.parent.remove_widget(list_item)

class LeftCheckbox(ILeftBody, MDCheckbox):
    pass

class ListItemWithDelete(OneLineRightIconListItem):
    def __init__(self, pk, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk


    def delete_ingridient(self, recipe_item):
        self.parent.remove_widget(recipe_item)

class RecipeCard(MDCard): #adding recipe cards to search screen
    def __init__(self, pk, name, source, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(FitImage(source=source, radius= ([20, 20, 0, 0])))
        self.pk = pk
        self.add_box = (BoxLayout(size_hint= (1, 0.2), padding=10))
        self.button = (
            MDFillRoundFlatIconButton(
                text= "Add",
                icon= "plus",
                text_color= "white"
        ))
        self.button.bind(on_release=lambda instance: app.request_list_item(instance, self.pk))
        self.add_box.add_widget(self.button)
        self.add_box.add_widget(
            MDLabel(
                text= name,
                halign= "right",
                theme_text_color= "Custom",
                text_color= "black",
                bold= "true",
                padding=10
        ))
        self.add_widget(self.add_box)



class CookAPP(MDApp):
    icon = "icon.ico"
    dialog = None
    file_manager = None
    my_list = []
    shopping_list = []
    picture_path = "def_picture.jpg"
    pk_for_list_item_in_recipe = -1
    def build(self): #creatibg all screens wth kivy
        self.theme_cls.primary_palette = "Red"
        self.sm = ScreenManager() #temporarily added inside app
        self.sm.add_widget(StartScreen(name='start'))
        self.sm.add_widget(SearchScreen(name='search'))
        self.sm.add_widget(RecipeScreen(name='recipe'))
        self.sm.add_widget(RecipeScreen(name='saved_recipe'))
        self.sm.add_widget(ListScreen(name='list'))
        self.help_str = Builder.load_string(Builder_string)
        return self.help_str
    

    def Add_item(self): #creating dialog to get items to shopping list act as additional screen
        if not self.dialog:
            self.dialog = MDDialog(
                title="Add Item",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="EXIT",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="ADD",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release= self.new_item_to_buy
                    ),
                ],
            )
        self.dialog.open()

    def new_item_to_buy(self, obj): #manually adding things to shopping list
        if self.dialog.content_cls.ids.data.text not in self.shopping_list:
            added = db.add_item(self.dialog.content_cls.ids.data.text, self.dialog.content_cls.ids.data_2.text)
            self.help_str.get_screen('list').ids.in_list.add_widget(ListItemWitchCheckbox(pk=int(added[0]), text = added[2] + "  " + added[1]))
            self.shopping_list.append(self.dialog.content_cls.ids.data.text)
            print(self.dialog.content_cls.ids.data.text)
        else:
            db.change_amount(self.dialog.content_cls.ids.data.text,self.dialog.content_cls.ids.data_2.text)
            self.help_str.get_screen('list').ids.in_list.clear_widgets()
            
            bought, unbought = db.get_items()

            if unbought != []:
                for item in unbought:
                    self.help_str.get_screen('list').ids.in_list.add_widget(ListItemWitchCheckbox(pk=int(item[0]), text = item[2] + "  " + item[1]))

            if bought != []:
                for item in bought:
                    add_item = (ListItemWitchCheckbox(pk=int(item[0]), text = item[2] + "  " + item[1]))
                    add_item.ids.check.active = True
                    self.help_str.get_screen('list').ids.in_list.add_widget(add_item)
        self.dialog.content_cls.ids.data.text = ""
        self.dialog.content_cls.ids.data_2.text = ""

    def close_dialog(self, *args): #support for dialog just function to close
        self.dialog.dismiss(force=True)
    
    def open_file_pick(self): #creating manager for picking files
        if not self.file_manager:
            self.file_manager = MDFileManager(
            select_path=self.select_path,
            exit_manager=self.exit_manager,
            preview=True)
        self.file_manager.show(pat)
	
    def select_path(self, path): #uploading photo
        self.picture_path=path
        self.help_str.get_screen('recipe').ids.layout.clear_widgets()
        self.help_str.get_screen('recipe').ids.layout.add_widget(FitImage(
                id="img",
                source= path,
                size_hint_y= .35,
                pos_hint= {"top": 1},
                radius= (0, 0, 40, 40)

            ))
        self.exit_manager(path)

    def exit_manager(self, path): #closing file manager
        self.file_manager.close()

    def add_ingridient(self, new_ingridient, new_ingridient_quantity): #support function 
        self.pk_for_list_item_in_recipe += 1
        dictio = {'id': self.pk_for_list_item_in_recipe, 'name': new_ingridient.text, 'quantity': new_ingridient_quantity.text}
        self.my_list.append(dictio)
        self.help_str.get_screen('recipe').ids.in_recipe.add_widget(ListItemWithDelete(pk=self.pk_for_list_item_in_recipe, text= new_ingridient_quantity.text + "   " + new_ingridient.text))
        new_ingridient.text = ""
        new_ingridient_quantity.text = ""

    def delete_from_list(self, id): #deleting from my shopping list
        for item in self.my_list:
            if item["id"] == id.pk:
                self.my_list.remove(item)
                return

    def add_new_recipe(self, name, description): #adding new recipies to database and calling ceate_recipe_tile 
        new_recipe = db.add_recipe(name.text, description.text, self.picture_path)
        self.create_recipe_tile(new_recipe[3], new_recipe[1], new_recipe[0])
        if self.my_list != []:
            for ingredient in self.my_list:
                db.add_ingredient(ingredient["name"], ingredient["quantity"], new_recipe[0])
        self.clear_recipe_screen()

    def create_recipe_tile(self, photo, name, id): #adding new recipies to your overall recipe list mainly for kivy side
        my_tile = RecipeCard(pk=int(id), name = name, source=photo)
        self.help_str.get_screen('search').ids.recipe_number.add_widget(my_tile)

    def search(self, text): #searchbar for recipies in search screen
        self.help_str.get_screen('search').ids.recipe_number.clear_widgets()

        if text.text == "":
            recipies = db.get_recipies()
            for recipe in recipies:
                self.create_recipe_tile(recipe[3], recipe[1], recipe[0])
        else:
            findings = db.search(text.text)
            for item in findings:
                self.create_recipe_tile(item[3], item[1], item[0])

    def on_start(self): #what program does when you hit start
        bought, unbought = db.get_items()

        if unbought != []:
            for item in unbought:
                self.help_str.get_screen('list').ids.in_list.add_widget(ListItemWitchCheckbox(pk=int(item[0]), text = item[2] + "  " + item[1]))
                self.shopping_list.append(item[1])

        if bought != []:
            for item in bought:
                add_item = (ListItemWitchCheckbox(pk=int(item[0]), text = item[2] + "  " + item[1]))
                add_item.ids.check.active = True
                self.help_str.get_screen('list').ids.in_list.add_widget(add_item)
                self.shopping_list.append(item[1])

        recipies = db.get_recipies()
        for recipe in recipies:
            self.create_recipe_tile(recipe[3], recipe[1], recipe[0]) #additional argument id

    def clear_recipe_screen(self): #just clearing input for recipies screen
        self.pk_for_list_item_in_recipe = -1
        self.picture_path = "def_picture.jpg"
        self.my_list = []
        self.help_str.get_screen('recipe').ids.recipe_name.text = ""
        self.help_str.get_screen('recipe').ids.recipe_description.text = ""
        self.help_str.get_screen('recipe').ids.layout.clear_widgets()
        self.help_str.get_screen('recipe').ids.in_recipe.clear_widgets()
        self.help_str.get_screen('recipe').ids.layout.add_widget(FitImage(
                id="img",
                source= "paper.jpg",
                size_hint_y= .35,
                pos_hint= {"top": 1},
                radius= (0, 0, 40, 40)

            ))
    
    def request_list_item(self, instance, id): #adding items to shopping list from search screen
        neded_ingredients = db.get_ingredients(id)
        for ingredient in neded_ingredients:
            if ingredient[1] not in self.shopping_list:
                added = db.add_item(ingredient[1], ingredient[2])
                self.help_str.get_screen('list').ids.in_list.add_widget(ListItemWitchCheckbox(pk=int(added[0]), text = added[2] + "  " + added[1]))
                self.shopping_list.append(added[1])
            else:
                db.change_amount(ingredient[1],ingredient[2])
                self.help_str.get_screen('list').ids.in_list.clear_widgets()
            
                bought, unbought = db.get_items()

                if unbought != []:
                    for item in unbought:
                        self.help_str.get_screen('list').ids.in_list.add_widget(ListItemWitchCheckbox(pk=int(item[0]), text = item[2] + "  " + item[1]))

                if bought != []:
                    for item in bought:
                        add_item = (ListItemWitchCheckbox(pk=int(item[0]), text = item[2] + "  " + item[1]))
                        add_item.ids.check.active = True
                        self.help_str.get_screen('list').ids.in_list.add_widget(add_item)
    
    def made_recipe_info(self, id): #loading particular recipe info
        self.help_str.get_screen('saved_recipe').ids.in_recipe.clear_widgets()
        details = db.recipe_details(id)
        self.help_str.get_screen('saved_recipe').ids.img.source = details[0][3]
        self.help_str.get_screen('saved_recipe').ids.recipe_name.text = details[0][1]
        self.help_str.get_screen('saved_recipe').ids.recipe_description.text = details[0][2]
        self.help_str.get_screen('saved_recipe').ids.add.bind(on_release=lambda instance: app.request_list_item(instance, id))
        self.help_str.get_screen('saved_recipe').ids.delete.bind(on_press=lambda instance: app.delete_recipe(instance, id))
        neded_ingredients = db.get_ingredients(id)
        for ingredient in neded_ingredients:
            self.help_str.get_screen('saved_recipe').ids.in_recipe.add_widget(OneLineListItem(text = ingredient[2] + "  " + ingredient[1]))

    def delete_recipe(self, instance, id):
        db.delete_recipe(id)
        self.help_str.get_screen('search').ids.recipe_number.clear_widgets()
        recipies = db.get_recipies()
        for recipe in recipies:
            self.create_recipe_tile(recipe[3], recipe[1], recipe[0])

if __name__ == "__main__":
    app = CookAPP()
    app.run()
