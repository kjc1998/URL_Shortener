<html>
	<head>
		<style>
			/* CSS comes here */
			body {
			    padding:20px;
			}
			
			.qr-btn {
			    background-color:#8c52ff;
			    padding:8px;
			    color:white;
			    cursor:pointer;
			}
		</style>
		
		<title>JavaScript QR Code Generator</title>
	</head>
	<body>
		<h3>QR Code Generator</h3>
        <div>
            <button class="qr-btn" onclick="generateQRCode()">Create QR Code</button>
        </div>
        <br/>
        <b>This is the QR code:</b>
        <p id="qr-result">No text given</p>
        
        
        <canvas id="qr-code"></canvas>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/qrious/4.0.2/qrious.min.js"></script>
		<script>
			/* JS comes here */
			var qr;
			(function() {
                    qr = new QRious({
                    element: document.getElementById('qr-code'),
                    size: 200,
                    value: 'https://studytonight.com'
                });
            })();
            
            function generateQRCode() {
                var qrtext = "https://www.w3schools.com/html/html_formatting.asp"
                document.getElementById("qr-result").innerHTML = "QR code for " + qrtext +":";
                alert(qrtext);
                qr.set({
                    foreground: 'black',
                    size: 200,
                    value: qrtext
                });
            }
		</script>
        
	</body>
</html>