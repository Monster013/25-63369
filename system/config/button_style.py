# button_style.py

# Define your button style variables
bttxt = "#ffffff"  # Button text color
btshado = "#ff00ff"  # Button shadow color
btcolor = "#6200ea"  # Button background color

# Function to return the HTML button code, passing ngrok_url as a parameter
def get_button_html(ngrok_url):
    showUrL = ngrok_url
    showTxT = f"Handbrake: {ngrok_url}"

    return f'''
    <style>
    @import url('https://fonts.googleapis.com/css?family=Source+Code+Pro:200,900');
    :root {{
        --text-color: {bttxt};
        --shadow-color: {btshado};
        --btn-color: {btcolor};
        --bg-color: #141218;
    }}
    * {{
        box-sizing: border-box;
    }}
    button {{
        position:relative;
        padding: 10px 20px;
        border: none;
        background: none;
        cursor: pointer;
        font-family: "Source Code Pro";
        font-weight: 900;
        font-size: 100%;
        color: var(--text-color);
        background-color: var(--btn-color);
        box-shadow: var(--shadow-color) 2px 2px 22px;
        border-radius: 4px;
        z-index: 0;
        overflow: hidden;
    }}
    button:focus {{
        outline-color: transparent;
        box-shadow: var(--btn-color) 2px 2px 22px;
    }}
    .right::after, button::after {{
        content: var(--content);
        display: block;
        position: absolute;
        white-space: nowrap;
        padding: 40px 40px;
        pointer-events:none;
    }}
    button::after{{
        font-weight: 200;
        top: -30px;
        left: -20px;
    }}
    .right, .left {{
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
    }}
    .right {{
        left: 66%;
    }}
    .left {{
        right: 66%;
    }}
    .right::after {{
        top: -30px;
        left: calc(-66% - 20px);
        background-color: var(--bg-color);
        color:transparent;
        transition: transform .4s ease-out;
        transform: translate(0, -90%) rotate(0deg)
    }}
    button:hover .right::after {{
        transform: translate(0, -47%) rotate(0deg)
    }}
    button .right:hover::after {{
        transform: translate(0, -50%) rotate(-7deg)
    }}
    button .left:hover ~ .right::after {{
        transform: translate(0, -50%) rotate(7deg)
    }}
    /* bubbles */
    button::before {{
        content: '';
        pointer-events: none;
        opacity: .6;
        background: radial-gradient(circle at 20% 35%,  transparent 0,  transparent 2px, var(--text-color) 3px, var(--text-color) 4px, transparent 4px),
                    radial-gradient(circle at 75% 44%, transparent 0,  transparent 2px, var(--text-color) 3px, var(--text-color) 4px, transparent 4px),
                    radial-gradient(circle at 46% 52%, transparent 0, transparent 4px, var(--text-color) 5px, var(--text-color) 6px, transparent 6px);
        width: 100%;
        height: 300%;
        top: 0;
        left: 0;
        position: absolute;
        animation: bubbles 5s linear infinite both;
    }}
    @keyframes bubbles {{
        from {{ transform: translate(); }}
        to {{ transform: translate(0, -66.666%); }}
    }}
    </style>
    <center>
    <a href="{showUrL}" target="_blank">
        <div style="width: 700px; height: 80px; padding-top:15px">
            <button style='--content: "{showTxT}";'>
                <div class="left"></div>{showTxT}<div class="right"></div>
            </button>
        </div>
    </a>
    </center>
    '''
