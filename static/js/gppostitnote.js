class GpPostitNote extends HTMLElement {
  static get observedAttributes() {
    return ['degrees', 'title'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.isOpen = false;
    this.shadowRoot.innerHTML = `
      <link href="https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap" rel="stylesheet">
          <style>
            :host {
              display: inline-block;
            }
            
            .rotate {
              transform: rotate(var(--rotation-deg));
              -webkit-transform: rotate(var(--rotation-deg));
              -moz-transform: rotate(var(--rotation-deg));
              -o-transform: rotate(var(--rotation-deg));
            }
            .postit {
              line-height: 1;
              text-align:center;     
              width: 475px;    
              margin: 25px;    
              min-height:150px;
              max-height:1250px;
              padding-top:5px;
              padding-bottom:25px;
              padding-left:15px;
              padding-right:15px;
              position:relative;   
              border:1px solid #E8E8E8;  
              border-top:60px solid #fdfd86;
              font-family: 'Patrick Hand', cursive;
              font-size:26px;      
              border-bottom-right-radius: 60px 5px;
              display:inline-block;    
              background: #ffff88; /* Old browsers */
              background: -moz-linear-gradient(-45deg, #ffff88 81%, #ffff88 82%, #ffff88 82%, #ffffc6 100%); /* FF3.6+ */
              background: -webkit-gradient(linear, left top, right bottom, color-stop(81%,#ffff88), color-stop(82%,#ffff88), color-stop(82%,#ffff88), color-stop(100%,#ffffc6)); /* Chrome,Safari4+ */
              background: -webkit-linear-gradient(-45deg, #ffff88 81%,#ffff88 82%,#ffff88 82%,#ffffc6 100%); /* Chrome10+,Safari5.1+ */
              background: -o-linear-gradient(-45deg, #ffff88 81%,#ffff88 82%,#ffff88 82%,#ffffc6 100%); /* Opera 11.10+ */
              background: -ms-linear-gradient(-45deg, #ffff88 81%,#ffff88 82%,#ffff88 82%,#ffffc6 100%); /* IE10+ */
              background: linear-gradient(135deg, #ffff88 81%,#ffff88 82%,#ffff88 82%,#ffffc6 100%); /* W3C */
              filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#ffff88', endColorstr='#ffffc6',GradientType=1 ); /* IE6-9 fallback on horizontal gradient */
            }
            
            .postit:after {     
              content: "";
              position:absolute;
              z-index:-1;
              right:-0px; bottom:20px;
              width:200px;
              height: 25px;
              background: rgba(0, 0, 0, 0.2);
              box-shadow:2px 15px 5px rgba(0, 0, 0, 0.40);
                -moz-transform: matrix(-1, -0.1, 0, 1, 0, 0);
             -webkit-transform: matrix(-1, -0.1, 0, 1, 0, 0);
                  -o-transform: matrix(-1, -0.1, 0, 1, 0, 0);
                 -ms-transform: matrix(-1, -0.1, 0, 1, 0, 0);
                     transform: matrix(-1, -0.1, 0, 1, 0, 0);
            }
            .title {
              font-weight: bold;
              margin-top: -45px;
            }
          </style>
          <div class="rotate">
              <div class="postit">
                  <header class="title">
                    <b>${this.getAttribute('title')}</b>
                  </header>
                  <section id="main">
                      <slot>default message</slot>
                  </section>        
              </div>
          </div>
      `;
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (name === 'degrees') {
      const postitElement = this.shadowRoot.querySelector('.rotate');
      postitElement.style.setProperty('--rotation-deg', newValue + 'deg');
    } else if (name === 'title') {
      const titleElement = this.shadowRoot.querySelector('.title b');
      titleElement.textContent = newValue || '';
    }
  }
}

customElements.define('gp-postit-note', GpPostitNote);