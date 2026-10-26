import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    valore_euro=0
    input_valore=ft.TextField(
        value=str(valore_euro),
        label="Valore",
        width=100,
        read_only=True,
        text_align=ft.TextAlign.CENTER
    )

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def decrementa_valore(e):
    #Decrementa il valore in euro dello strumento (senza scendere sotto 0)
        nonlocal valore_euro
        if valore_euro >= 10:
            valore_euro -= 10
        else:
            valore_euro = 0
            input_valore.value = str(valore_euro)
            page.update()

    input_tipo = ft.TextField(label="Tipo di strumento", width=200)
    input_marca = ft.TextField(label="Marca", width=200)
    input_anno = ft.TextField(label="Anno di acquisto", width=200)



    def incrementa_valore(e):
        #Incrementa il valore in euro dello strumento di 10€
        nonlocal valore_euro
        valore_euro += 10
        input_valore.value = str(valore_euro)
        page.update()

    def aggiungi_nuovo_strumento(e):
        #valida i dati dei TextField e aggiunge il nuovo strumento al deposito
        nonlocal valore_euro

        tipo = input_tipo.value.strip() if input_tipo.value else ""
        marca = input_marca.value.strip() if input_marca.value else ""
        anno_str = input_anno.value.strip() if input_anno.value else ""

        #verifica che i campi non siano vuoti
        if not tipo or not marca or not anno_str:
            alert.show_alert("Tutti i campi (Tipo, Marca, Anno) devono essere compilati!")
            return

        #Verifica che il campo Anno sia un numero intero valido
        if not anno_str.isdigit():
            alert.show_alert("L'anno di acquisto deve essere un numero intero valido!")
            return
        anno = int(anno_str)

        #Aggiunta dello strumento nella struttura dati del deposito
        try:
            deposito.aggiungi_strumento(tipo, marca, anno, float(valore_euro))

        #Svuotamento e reset dei campi TextField e del contatore
            input_tipo.value = ""
            input_marca.value = ""
            input_anno.value = ""
            valore_euro = 0
            input_valore.value = "0"

        #Aggiornamento della ListView a schermo
            aggiorna_lista_strumenti()
        except Exception as ex:
            alert.show_alert(f"Errore durante l'aggiunta dello strumento: {ex}")


    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    btn_meno = ft.IconButton(ft.Icons.REMOVE, on_click=decrementa_valore)
    btn_piu = ft.IconButton(ft.Icons.ADD, on_click=incrementa_valore)
    pulsante_aggiungi_strumento = ft.Button("Aggiungi strumento", on_click=aggiungi_nuovo_strumento)

    row_contatore = ft.Row(
        controls=[btn_meno, input_valore, btn_piu],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),
        ft.Text("Aggiungi Nuovo Strumento", size=20, weight=ft.FontWeight.BOLD),
        ft.Row(
            controls=[btn_meno, input_valore, btn_piu],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Text("Valore dello strumento (€):"),
        row_contatore,
        pulsante_aggiungi_strumento,

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
