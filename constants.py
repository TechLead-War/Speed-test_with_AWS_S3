class Constants:
    bucket_name = "speed-test-bucket-01"
    file = 'network_testfile'
    region = 'ap-south-1'


class HTML:
    render_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
    
            .container {
                text-align: center;
                padding: 20px;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
    
            h1 {
                color: #333;
            }
    
            button {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
            }
    
            button:hover {
                background-color: #0056b3;
            }
    
            p {
                margin: 10px 0;
            }
    
            /* Add the following CSS for the R&D text */
            .footer {
                position: fixed;
                bottom: 10px;
                right: 10px;
                color: #888;
            }
        </style>
    </head>
    <body>
    <div class="container">
        <h1>Speed Test,</h1> an unbiased network app.<br><br>
        <button id="start-test">Start Speed Test</button>
        <div id="result">
            <p><strong>Upload Path:</strong> <span id="path"></span></p>
            <p><strong>Time Taken:</strong> <span id="time-taken"></span> seconds</p>
            <p><strong>Upload Speed:</strong> <span id="upload-speed"></span> MB/sec</p>
        </div>
    </div>
    <!-- Add the R&D text here -->
    <div class="footer">Product of - R&D Labs (Kapnet)</div>
    <script>
        document.getElementById("start-test").addEventListener("click", function() {
            fetch('/upload_file', {
                method: 'POST'  // Specify the HTTP method as POST
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("path").textContent = data.path;
                document.getElementById("time-taken").textContent = data.time_taken;
                document.getElementById("upload-speed").textContent = data.average_speed;
            });
        });
    </script>
    </body>
</html>
"""