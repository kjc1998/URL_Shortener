const navSlide = () => {
    const burger = document.querySelector('.burgerView');
    const nav = document.querySelector('.rightSide');
    const rightSides = document.querySelectorAll('.rightSide li');
    //toggle
    burger.addEventListener('click', ()=>{
        nav.classList.toggle('nav-active');

        //Animation
        rightSides.forEach((link, index)=>{
            if (link.style.animation) {
                link.style.animation = ''
            } else {
                link.style.animation = `navLinkFade 0.5s ease forwards ${index/ 5 + 0.5}s`
            }
        });
        //burger animation
        burger.classList.toggle('toggle');
        if(document.getElementById("scrollDiv").style.overflow === "hidden"){
          nav.style.position = "";
          document.getElementById("scrollDiv").style.overflow = "scroll";
        }else{
          nav.style.position = "fixed";
          document.getElementById("scrollDiv").style.overflow = "hidden";
        }
    });
    
    
}

navSlide();


//Container
if (screen.width > 768){
  (function() {
      // Init
      var container = document.getElementById("container_trans"),
          inner = document.getElementById("inner");
    
      // Mouse
      var mouse = {
        _x: 0,
        _y: 0,
        x: 0,
        y: 0,
        updatePosition: function(event) {
          var e = event || window.event;
          this.x = e.clientX - this._x;
          this.y = (e.clientY - this._y) * -1;
        },
        setOrigin: function(e) {
          this._x = e.offsetLeft + Math.floor(e.offsetWidth / 2);
          this._y = e.offsetTop + Math.floor(e.offsetHeight / 2);
        },
        show: function() {
          return "(" + this.x + ", " + this.y + ")";
        }
      };
    
      // Track the mouse position relative to the center of the container.
      mouse.setOrigin(container);
    
      //----------------------------------------------------
    
      var counter = 0;
      var refreshRate = 10;
      var isTimeToUpdate = function() {
        return counter++ % refreshRate === 0;
      };
    
      //----------------------------------------------------
    
      var onMouseEnterHandler = function(event) {
        update(event);
      };
    
      var onMouseLeaveHandler = function() {
        inner.style = "";
      };
    
      var onMouseMoveHandler = function(event) {
        if (isTimeToUpdate()) {
          update(event);
        }
      };
    
      //----------------------------------------------------
    
      var update = function(event) {
        mouse.updatePosition(event);
        updateTransformStyle(
          (mouse.y / inner.offsetHeight / 2).toFixed(2),
          (mouse.x / inner.offsetWidth / 2).toFixed(2)
        );
      };
    
      var updateTransformStyle = function(x, y) {
        var style = "rotateX(" + x + "deg) rotateY(" + y + "deg)";
        inner.style.transform = style;
        inner.style.webkitTransform = style;
        inner.style.mozTranform = style;
        inner.style.msTransform = style;
        inner.style.oTransform = style;
      };
    
      //--------------------------------------------------------
    
      container.onmousemove = onMouseMoveHandler;
      container.onmouseleave = onMouseLeaveHandler;
      container.onmouseenter = onMouseEnterHandler;
  })();
}


document.getElementById('scrollDiv').addEventListener(
  'scroll',
  function(){
      var y = document.getElementById('scrollDiv').scrollTop;
      if (y >= 500){
      document.getElementById('scrollAppear').className = "back show";
      }else{
      document.getElementById('scrollAppear').className = "back hide";
      }
      console.log(y);
  }
);