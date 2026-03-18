import customtkinter as ctk
import sqlite3

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app=ctk.CTk()
app.geometry("650x750")
app.title("Wall Street Terminal")

#content

main_scroll_frame=ctk.CTkScrollableFrame(app)
main_scroll_frame.pack(fill="both",expand=True,padx=10,pady=10)

title_label=ctk.CTkLabel(main_scroll_frame,text="Coporate Inventory Ledgar",font=("Arial",24,"bold"))
title_label.pack(pady=20)

display_box=ctk.CTkTextbox(main_scroll_frame,width=550,height=250,font=("Courier",14))
display_box.pack(pady=10)

analytics_box=ctk.CTkTextbox(main_scroll_frame,width=550,height=130,font=("Courier",14),fg_color="#1A2B3C",text_color="#00FFCC")
analytics_box.pack(pady=19)
analytics_box.insert("end","Awaiting Analytics...\n")
def load_data():
    display_box.delete("0.0","end")

    conn=sqlite3.connect("finance_ledger.db")
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM inventory_ledger")
    records= cursor.fetchall()

    display_box.insert("end",f"{'ID':<5}|{'PRODUCT':<15}|{'UNITS':<6}|{'PRICE':<8}|{'TYPE'}\n")
    display_box.insert("end","-"*65+"\n")

    for row in records:
        formatted_row=f"{row[0]:<5}|{row[1]:<15}|{row[2]:<6}|${row[3]:<7.2f}|{row[4]}\n"
        display_box.insert("end",formatted_row)

    conn.close()

def run_analytics():
    conn=sqlite3.connect("finance_ledger.db")
    cursor=conn.cursor()
    cursor.execute("SELECT product_name,units,unit_price,transaction_type FROM inventory_ledger")
    records=cursor.fetchall()

    conn.close()

    total_revenue=0
    total_cogs=0
    inventory_value=0
    unit_costs={}

    for name,units,price,t_type in records:
        if t_type=="RESTOCK":
            unit_costs[name]=price
            inventory_value+=(units*price)
        
        elif t_type=="SALE":
            total_revenue+=(units*price)

            if name in unit_costs:
                cogs_for_this_sal = units * unit_costs[name]
            else:
                cogs_for_this_sal = 0 

            total_cogs+=cogs_for_this_sal
            inventory_value-=cogs_for_this_sal
    
    avg_inventory=inventory_value/2
    turnover_ratio=total_cogs/avg_inventory if avg_inventory>0 else 0
    gross_profit=total_revenue-total_cogs

    analytics_box.delete("0.0","end")
    analytics_box.insert("end",f"{'---FINANCIAL METRICS---':^50}\n\n")
    analytics_box.insert("end", f"Total Revenue:       ${total_revenue:,.2f}\n")
    analytics_box.insert("end", f"Cost of Goods Sold:  ${total_cogs:,.2f}\n")
    analytics_box.insert("end", f"Gross Profit:        ${gross_profit:,.2f}\n")
    analytics_box.insert("end", f"Ending Inventory:    ${inventory_value:,.2f}\n")
    analytics_box.insert("end", f"Inventory Turnover:  {turnover_ratio:.2f}\n")

def add_transaction():
    prod_name=name_entry.get()
    prod_units=units_entry.get()
    prod_price=price_entry.get()
    trans_type=type_dropdown.get()

    if not prod_name or not prod_units or not prod_price:
        print("Please fill up all field")
        return
    
    conn=sqlite3.connect("finance_ledger.db")
    cursor=conn.cursor()

    cursor.execute("INSERT INTO inventory_ledger (product_name, units, unit_price, transaction_type) VALUES (?, ?, ?, ?)", 
                   (prod_name, int(prod_units), float(prod_price), trans_type))
    
    conn.commit()
    conn.close()
    
    name_entry.delete(0,"end")
    units_entry.delete(0,"end")
    price_entry.delete(0,"end")

    load_data()
    run_analytics()

def delete_transaction():
    target_id=delete_entry.get()

    if not target_id:
        print("Please enter an ID to delete!")
        return
    
    conn=sqlite3.connect("finance_ledger.db")
    cursor=conn.cursor()

    cursor.execute("DELETE FROM inventory_ledger WHERE id = ?",(int(target_id),))
    conn.commit()
    conn.close()

    delete_entry.delete(0,"end")
    load_data()
    run_analytics()

button_frame=ctk.CTkFrame(main_scroll_frame,fg_color="transparent")
button_frame.pack(pady=10)

load_button=ctk.CTkButton(
    button_frame,
    text="Fetch Database Record",
    command=load_data,
    fg_color="#27AE60",
    hover_color="#1E8449"
)
load_button.grid(row=0,column=0,padx=10)

analytics_button=ctk.CTkButton(button_frame,text="2. Run Analytics",command=run_analytics,fg_color="#E67E22",hover_color="#D35400")
analytics_button.grid(row=0,column=1,padx=10)

input_frame=ctk.CTkFrame(main_scroll_frame)
input_frame.pack(pady=10,padx=20,fill="both")
input_frame.grid_columnconfigure((0,1,2,3),weight=1)

name_entry=ctk.CTkEntry(input_frame,placeholder_text="Product Name",width=140)
name_entry.grid(row=0,column=0,padx=5,pady=10)

units_entry=ctk.CTkEntry(input_frame,placeholder_text="Units (e.g.10)",width=100)
units_entry.grid(row=0,column=1,padx=5,pady=10)

price_entry=ctk.CTkEntry(input_frame,placeholder_text="Price (e.g. 50.50)",width=120)
price_entry.grid(row=0,column=2,padx=5,pady=10)

type_dropdown=ctk.CTkOptionMenu(input_frame,values=["RESTOCK","SALE"],width=100)
type_dropdown.grid(row=0,column=3,padx=5,pady=10)

submit_button=ctk.CTkButton(input_frame,text="➕ Add Transaction",command=add_transaction,fg_color="#2980B9",hover_color="#1F618D",width=200)
submit_button.grid(row=1,column=0,columnspan=4,pady=10)

delete_frame=ctk.CTkFrame(main_scroll_frame)
delete_frame.pack(padx=10)

delete_entry=ctk.CTkEntry(delete_frame,placeholder_text="Enter ID to Delete",width=140)
delete_entry.grid(row=0,column=0,padx=10)

delete_button=ctk.CTkButton(delete_frame,text="🗑️ Delete ID",command=delete_transaction,fg_color="#C0392B",hover_color="#922B21")
delete_button.grid(row=0,column=1,padx=10)
app.mainloop()