import flet as ft
import pickle
import sys

def collect_data():

    def main(page: ft.Page):


        def selected_conf(e):
            # output_text.value = conf_dropdown.value
            if(conf_dropdown.value == "Yes"):
                cond_T.disabled = True
                fluid_h.disabled = False
                fluid_T.disabled = False
            else:
                cond_T.disabled = False
                fluid_h.disabled = True
                fluid_T.disabled = True
            page.update()

        def eselected_conf(e):
            # output_text.value = east_dropdown.value
            if(east_dropdown.value == "Yes"):
                econd_T.disabled = True
                efluid_h.disabled = False
                efluid_T.disabled = False
            else:
                econd_T.disabled = False
                efluid_h.disabled = True
                efluid_T.disabled = True
            page.update()

        def sselected_conf(e):
            # output_text.value = south_dropdown.value
            if(south_dropdown.value == "Yes"):
                scond_T.disabled = True
                sfluid_h.disabled = False
                sfluid_T.disabled = False
            else:
                scond_T.disabled = False
                sfluid_h.disabled = True
                sfluid_T.disabled = True
            page.update()
        
        def wselected_conf(e):
            # output_text.value = west_dropdown.value
            if(west_dropdown.value == "Yes"):
                wcond_T.disabled = True
                wfluid_h.disabled = False
                wfluid_T.disabled = False
            else:
                wcond_T.disabled = False
                wfluid_h.disabled = True
                wfluid_T.disabled = True
            page.update()

        def end_progr(e):
            # gather data to return later
            Help = [conf_dropdown, east_dropdown, south_dropdown, west_dropdown]
            Help2 = [fluid_h.value, efluid_h.value, sfluid_h.value, wfluid_h.value]
            Help3 = [fluid_T.value, efluid_T.value, sfluid_T.value, wfluid_T.value]
            Help4 = [cond_T.value, econd_T.value, scond_T.value, wcond_T.value]
            #prepare the data to fit on the application's model
            confs = []
            data = []
            lx = float(dim1.value)
            ly = float(dim2.value)
            nx = int(mesh1.value)
            ny = int(mesh2.value)
            term = float(k.value)
            for j in range(0, 4):
                if(Help[j].value == "Yes"):
                    confs.append('y')
                    data.append( (float(Help3[j]), float(Help2[j])) )
                else:
                    confs.append('n')
                    data.append( (float(Help4[j]), float(Help2[j])) )
            output_text.value = data
            page.update()

            ret = {'con': confs, 'dat': data, 'lx':lx, 'ly': ly, 'nx': nx, 'ny': ny, 'k': term}

            with open('data.npy', 'wb') as f:
                pickle.dump(ret, f)

            sys.exit()
            # return confs, data, lx, ly, nx, ny, term


        #1st boundary
        FrN = ft.Text("Does the North boundary interact with a fluid?")
        conf_dropdown = ft.Dropdown(
            width=100,
            options=[
                ft.dropdown.Option("Yes"),
                ft.dropdown.Option("No"),
            ],
            on_change=selected_conf
        )
        
        fluid_h = ft.TextField(value="0", label="Fluid conduction heat transfer coefficient (h)", autofocus=True)
        fluid_T = ft.TextField(value="0", label="Fluid Temperature")
        cond_T = ft.TextField(value="0", label="Border Temperature")
        fst_items = ft.Row([conf_dropdown, fluid_h, fluid_T, cond_T], alignment=ft.MainAxisAlignment.CENTER)
        output_text = ft.Text()

        # 2nd boundary

        FrE = ft.Text(f"Does the East boundary interact with a fluid?")
        east_dropdown = ft.Dropdown(
            width=100,
            options=[
                ft.dropdown.Option("Yes"),
                ft.dropdown.Option("No"),
            ],
            on_change=eselected_conf
        )    
        efluid_h = ft.TextField(value="0", label="Fluid conduction heat transfer coefficient (h)")
        efluid_T = ft.TextField(value="0", label="Fluid Temperature")
        econd_T =  ft.TextField(value="0", label="Border Temperature")
        scnd_items = ft.Row([east_dropdown, efluid_h, efluid_T, econd_T], alignment=ft.MainAxisAlignment.CENTER)
        # output_text = ft.Text()

        # 3rd boundary

        FrS = ft.Text(f"Does the South boundary interact with a fluid?")
        south_dropdown = ft.Dropdown(
            width=100,
            options=[
                ft.dropdown.Option("Yes"),
                ft.dropdown.Option("No"),
            ],
            on_change=sselected_conf
        )
        
        sfluid_h = ft.TextField(value="0", label="Fluid conduction heat transfer coefficient (h)")
        sfluid_T = ft.TextField(value="0", label="Fluid Temperature")
        scond_T = ft.TextField(value="0", label="Border Temperature")
        trd_items = ft.Row([south_dropdown, sfluid_h, sfluid_T, scond_T], alignment=ft.MainAxisAlignment.CENTER)
        # output_text = ft.Text()

        # 4th boundary

        FrW = ft.Text(f"Does the West boundary interact with a fluid?")
        west_dropdown = ft.Dropdown(
            width=100,
            options=[
                ft.dropdown.Option("Yes"),
                ft.dropdown.Option("No"),
            ],
            on_change=wselected_conf
        )
        
        wfluid_h = ft.TextField(value="0", label="Fluid conduction heat transfer coefficient (h)")
        wfluid_T = ft.TextField(value="0", label="Fluid Temperature")
        wcond_T = ft.TextField(value="0", label="Border Temperature")
        fth_items = ft.Row([west_dropdown, wfluid_h, wfluid_T, wcond_T], alignment=ft.MainAxisAlignment.CENTER)

        # Conductor's dimensions

        dim = ft.Text("Conductor's dimensions")
        dim1 = ft.TextField(value="0", label="x dimension", width=100)
        dim2 = ft.TextField(value="0", label="y dimension", width=100)

        #  Thermal Conductivity

        K = ft.Text("Thermal Conductivity")
        k = ft.TextField(value="0", label="Thermal Cond.", width=100)

        # Mesh Field Dimensions

        MESH = ft.Text("Mesh Field dimensions")
        mesh1 = ft.TextField(value="0", label="x dimension", width=100)
        mesh2 = ft.TextField(value="0", label="y dimension", width=100) 

        a1 = ft.Row([dim1, dim2])
        a2 = ft.Row([mesh1, mesh2])
        c1 = ft.Column([dim, a1], alignment=ft.MainAxisAlignment.CENTER)
        c2 = ft.Column([K, k], alignment=ft.MainAxisAlignment.CENTER)
        c3 = ft.Column([MESH, a2], alignment=ft.MainAxisAlignment.CENTER)
        Frow = ft.Row([c1, c2, c3], alignment=ft.MainAxisAlignment.CENTER)

        r = ft.Row(wrap=True, scroll="always", expand=True)

        com = [ft.Column([ft.Row([FrN], alignment=ft.MainAxisAlignment.CENTER), fst_items], alignment=ft.MainAxisAlignment.CENTER),
        ft.Column([ft.Row([FrE], alignment=ft.MainAxisAlignment.CENTER), scnd_items], alignment=ft.MainAxisAlignment.CENTER), 
        ft.Column([ft.Row([FrS], alignment=ft.MainAxisAlignment.CENTER), trd_items], alignment=ft.MainAxisAlignment.CENTER), 
        ft.Column([ft.Row([FrW], alignment=ft.MainAxisAlignment.CENTER), fth_items], alignment=ft.MainAxisAlignment.CENTER), 
        Frow]

        for i in range(5):
            r.controls.append(
                ft.Container(
                    com[i],
                    width=1500,
                    height=150,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.WHITE,
                    border=ft.border.all(1, ft.colors.BLACK12),
                    border_radius=ft.border_radius.all(5),
                )
            )

        page.add(
            r,
            output_text,
            ft.ElevatedButton(text="Submit", on_click=end_progr)
        )

    ft.app(target=main)


#Possível solução: salve os dados finais na session do flet e, ao clicar em um botão de finalizar, retorne os dados da session e feche-a