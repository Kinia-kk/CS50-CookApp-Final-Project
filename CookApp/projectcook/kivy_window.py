Builder_string = """

ScreenManager:
    StartScreen:
    SearchScreen:
    RecipeScreen:
    SavedRecipeScreen:
    ListScreen:                 
 
<StartScreen>:
    name: 'start'
    FitImage:
        source: "cooking.jpg"
        size_hint_y: .35
        pos_hint: {"top": 1}
        radius: 0, 0, 40, 40
    BoxLayout:
        pos_hint: {"center_x": 0.56, "top": 0.8}
        spacing: "40dp"
        size_hint: .7, .7
        orientation: 'vertical'
        MDLabel:
            text: "Cook App"
            font_size: 80
            size_hint: .8, .03
            halign: "center"
        MDCard:
            md_bg_color: "blue"
            size_hint: .8, .05
            radius: 12
            elevation: 5
            FitImage:
                source: "shopping.jpg"
                radius: 12

        MDCard:
            md_bg_color: "blue"
            size_hint: .8, .05
            radius: 12
            elevation: 5
            FitImage:
                source: "fish.jpg"
                radius: 12
    MDRaisedButton:
        text: "List"
        on_press: root.manager.current = 'list'
        md_bg_color: "red"
        pos_hint: {"center_x": 0.5, "top": 0.53}
        size_hint: .2, .01
        font_size: "12sp"
    MDRaisedButton:
        text: "Recipes"
        on_press: root.manager.current = 'search'
        md_bg_color: "red"
        pos_hint: {"center_x": 0.5, "top": 0.25}
        size_hint: .2, .01
        font_size: "12sp"
        
<SearchScreen>:
    name: 'search'
    FitImage:
        source: "salad.jpg"
        size_hint_y: .35
        pos_hint: {"top": 1}
        radius: 0, 0, 40, 40
    MDFloatingActionButton:
        icon: "menu"
        pos_hint: {"x": 0.02, "top": 0.98}
        on_release: root.manager.current = 'list'
    MDLabel:
        font_size: 60
        text: "Recipes"
        pos_hint: {"y": 0.3, "x": 0.1}
        theme_text_color: "Custom"
        text_color: "white"
    MDTextField:
        hint_text: "Search"
        id: search
        mode: "round"
        size_hint: 0.5, 0.06
        pos_hint: {"center_x": .3, "center_y": .7}
        on_text: app.search(self)
    ScrollView:
        pos_hint: {"center_y": 0.3, "center_x": 0.5}
        size_hint: 0.8, 0.6
        MDGridLayout:
            pos_hint: {"center_y": 0.12, "center_x": 0.5}
            cols: 1
            id: recipe_number
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            size_hint_y: None
            height: self.minimum_height
            adaptive_height: True
            spacing: "20dp"
    MDFloatingActionButton:
        icon: "plus-thick"
        on_press: root.manager.current = 'recipe'
        pos_hint: {"x": 0.45, "y": 0.04}
    


<RecipeScreen>:
    name: 'recipe'
    MDScreen:
        BoxLayout:
            id: layout
            FitImage:
                id: img
                source: "paper.jpg"
                size_hint_y: .35
                pos_hint: {"top": 1}
                radius: 0, 0, 40, 40
        MDRectangleFlatButton:
            text: "Select image"
            pos_hint: {"center_x": .5, "top": .9}
            on_press: app.open_file_pick()
        MDFloatingActionButton:
            icon: "undo-variant"
            pos_hint: {"x": 0.02, "top": 0.98}
            on_press: app.clear_recipe_screen()
            on_release: root.manager.current = 'search'
        MDFillRoundFlatButton:
            text: "Save"
            on_press: (app.add_new_recipe(recipe_name, recipe_description))
            text_color: "white"
            pos_hint: {"x": .8, "top": 0.98}
        
        MDCard:
            pos_hint: {"center_x": .5, "center_y": .4}
            size_hint: 0.8, 0.8
            radius: 20, 20, 20, 20
            orientation: 'vertical'
            MDTextField:
                id: recipe_name
                hint_text: "Recipe title"
                mode: "fill"
                pos_hint: {"y": 1}
                size_hint: 1, .3
        
                
            BoxLayout:
                size_hint: .9, .35
                pos_hint: {"center_x": .5, "center_y": .5}
                MDTextField:
                    id: new_ingridient
                    size_hint: .2, 1
                    hint_text: "Ingredient"
                MDTextField:
                    id: new_ingridient_quantity
                    size_hint: .2, 1
                    hint_text: "Quantity"
                MDRaisedButton:
                    text: "Add"
                    size_hint: .1, .7
                    on_press: app.add_ingridient(new_ingridient, new_ingridient_quantity)
            ScrollView:
                pos_hint: {"center_x": .55, "center_y": .5}
                orientation: 'vertical'
                size_hint: .9, .5
                MDList:
                    id: in_recipe
                    size_hint_y: None
                    height: self.minimum_height
            MDTextField:
                id: recipe_description
                hint_text: "Description"
                multiline: True
                mode: "rectangle"
                size_hint: 1, .8

                
<SavedRecipeScreen>:
    name: 'saved_recipe'
    FitImage:
        id: img
        source: "cooking.jpg"
        size_hint_y: .35
        pos_hint: {"top": 1}
        radius: 0, 0, 40, 40
    MDFloatingActionButton:
        icon: "undo-variant"
        pos_hint: {"x": 0.02, "top": 0.98}
        on_press: root.manager.current = 'search'
    MDFillRoundFlatButton:
        id: delete
        on_release: root.manager.current = 'search'
        text: "Delete"
        text_color: "white"
        pos_hint: {"x": .77, "top": 0.98}
    ScrollView
        pos_hint: {"center_x": .5, "center_y": .4}
        size_hint: 0.8, 0.8
        MDCard:
            spacing: 50
            orientation: 'vertical'
            pos_hint: {"center_x": .5, "center_y": .4}
            id: layout
            radius: 20, 20, 20, 20
            padding: 30
            size_hint_y: None
            height: self.minimum_height
            MDLabel:
                id: recipe_name
                pos_hint: {"center_x": .5, "y": .8}
                text: "Recipe title"
                size_hint_y: None
                text_size: self.width, None
                height: self.texture_size[1]
            MDList:
                size_hint: .9, .5
                id: in_recipe
                size_hint_y: None
                text_size: self.width, None
                height: self.height
            MDLabel:
                id: recipe_description
                text: "description"
                size_hint_y: None
                text_size: self.width, None
                height: self.texture_size[1]
    MDFillRoundFlatIconButton:
        id: add
        text: "Add"
        icon: "plus"
        text_color: "white"
        pos_hint: {"center_x": .85, "y": .025}
                    


<ListScreen>:
    name: 'list'
    MDFloatLayout:
        MDFloatingActionButton:
            icon: "menu"
            pos_hint: {"x": 0.02, "top": 0.98}
            on_release: root.manager.current = 'search'
        MDLabel:
            halign: "center"
            font_size: 60
            text: "Shoppig List"
            pos_hint: {"y": 0.43}
        ScrollView:
            pos_hint: {"center_y": 0.5, "center_x": 0.5}
            size_hint: 0.9, 0.8
            MDList:
                id: in_list
        MDFloatingActionButton:
            icon: "plus-thick"
            on_release: app.Add_item()
            pos_hint: {"x": 0.45, "y": 0.04}
                    
<Content>
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"
    BoxLayout:
        MDTextField:
            id:data
            hint_text: "Item"
        MDTextField:
            id:data_2
            hint_text: "Quantity"


<ListItemWitchCheckbox>
    id: list_item
    markup: True
    LeftCheckbox:
        id: check
        on_release: root.mark(check, list_item)
    IconRightWidget:
        icon: "trash-can-outline"
        theme_text_color: "Custom"
        text_color: 1, 0, 0, 1
        on_release: root.delete_item(list_item)

<ListItemWithDelete>
    id: recipe_item
    padding: "Custom"
    padding: .1
    markup: True
    IconRightWidget:
        pos_hint: {"x": 1}
        icon: "trash-can-outline"
        theme_text_color: "Custom"
        text_color: 1, 0, 0, 1
        on_release: (root.delete_ingridient(recipe_item), app.delete_from_list(recipe_item))

<My_recipe>
    id: my_recipe
    orientation: 'vertical'
    radius: 20, 20, 20, 20
    size_hint: .8, .5

<MyrecipeCard>
    id: recipe_card
    radius: 20, 20, 20, 20
    size_hint: .8, .5
    FitImage:
        source: self.source
    MDBoxLayout:
        pos_hint: {"x": .5}
        padding: 50
        MDLabel:
            text: self.name
            padding: 50
        MDFillRoundFlatIconButton:
            icon: "plus"
            text: "Add"
            pos_hint: {"x": .5}

<RecipeCard>
    radius: 20 
    box_radius: [20, 20, 20, 20]
    size_hint: .5, .2
    orientation: 'vertical'
    pos_hint: {"center_x": .5, "center_y": .5}
    on_press: app.made_recipe_info(self.pk)
    on_release: app.root.current = 'saved_recipe'
"""
