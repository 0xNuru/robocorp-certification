import time

from robocorp.tasks import task
from robocorp import browser
from robocorp.browser import page
from RPA.Archive import Archive
from RPA.HTTP import HTTP
from RPA.Tables import Tables, Table
from RPA.PDF import PDF


archive = Archive()
http = HTTP()
tables = Tables()
pdf = PDF()

@task
def order_robots_from_RSB():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    page = open_robot_order_website()
    close_annoying_modal(page)
    orders_table = get_orders()
    for order in orders_table:
        fill_form(page, order)
        preview_order(page)
        submit_order(page)
        order_number = page.locator("p[class='badge badge-success']").inner_text()
        store_receipt_as_pdf(page, order_number)
        screenshot_robot(page, order_number)
        embed_screenshot_to_receipt(order_number)
        order_another_robot(page)
        close_annoying_modal(page)
    archive_receipts()


def open_robot_order_website() -> page:
    """open RSB"""
    browser.configure(slowmo=100)
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

    return browser.page()

def close_annoying_modal(page):
    """close annoying modal"""
    page.click("css=.alert-buttons button:text('OK')")


def get_orders() -> Table:
    """download orders csv"""
    http.download(url="https://robotsparebinindustries.com/orders.csv", target_file="data/orders.csv", overwrite=True)
    orders_table = tables.read_table_from_csv(path="data/orders.csv", header=True)
    return orders_table


def fill_form(page, order):
    """fill form with order passed as argument"""
    page.select_option("#head", str(order["Head"]))
    body_selector = f"input[name='body'][value='{int(order['Body'])}']"
    page.click(body_selector)
    page.fill("input[placeholder='Enter the part number for the legs']", str(order["Legs"]))
    page.fill("input[id='address']", order["Address"])

def preview_order(page):
    """preview the robot we're want to order"""
    page.click("button[id='preview']")

def submit_order(page):
    """submit order"""
    while True:
        page.click("button[id='order']")
        time.sleep(0.1) 

        if page.query_selector("div[class='alert alert-danger']") is None:
            break

        print("Retrying")

def store_receipt_as_pdf(page, order_number) -> str:
    """store receipt div from the website in pdf"""
    reciept_html = page.locator("#receipt").inner_html()
    pdf.html_to_pdf(reciept_html, f"output/receipts/{order_number}.pdf")


def screenshot_robot(page, order_number):
    """Take a screenshot of the robot preview"""
    element = page.query_selector("#robot-preview-image")
    element.screenshot(path=f"output/previews/{order_number}.png")

def embed_screenshot_to_receipt(order_number):
    """append screenshot to receipt"""
    receipt = f"output/receipts/{order_number}.pdf"
    screeenshot = f"output/previews/{order_number}.png"
    pdf.add_watermark_image_to_pdf(image_path=screeenshot, source_path=receipt, output_path=receipt, coverage=0.2)


def order_another_robot(page):
    """order another robot"""
    page.click("button[id='order-another']")

def archive_receipts():
    """create a zip archive of receipts"""
    archive.archive_folder_with_zip("output/receipts", "output/receipts.zip", recursive=True)

    
