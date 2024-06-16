function findsp24()
{
    var netID = document.getElementById('netID').value.trim().toLowerCase();
    var code = document.getElementById('code').value.trim();
    var url = 'https://cards.cornelllifted.com/pdfs/sp24/' + encodeURIComponent(netID) + '_' + encodeURIComponent(code) + ".pdf";

    window.open(url);
}