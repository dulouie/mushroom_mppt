let sketch = function(p) {
  let img;
  let paint = false;
  let mpp = false;

  p.preload = function() {
    img = p.loadImage('dist/pictures/iu-kennlinie.png');
  }

  p.setup = function() {
    let cnv = p.createCanvas(600, 400);
    cnv.parent('iukenn1');
  }

    p.draw = function() {
      let myDegrees = p.map(p.mouseY, 0, p.height, 250, 400);
      let v = p5.Vector.fromAngle(p.radians(myDegrees), 500);
      let vx = v.x;
      let vy = v.y;

      p.background(255)
      p.image(img,0,0)
      p.strokeWeight(3)
      p.stroke(255,0,0)
      p.translate(75,350)

      if (mpp == true){
        vx = 400
        vy = -300
        p.circle(350, -260, 20);
      }

      if (paint == true) {
        p.line(0,0,vx,vy);
      }
    }

  p.mouseClicked = function() {
    if (paint == false){
      paint = true;
    } else {
      paint = false;
    }
  }

  p.keyPressed = function(){
    if (p.keyCode === p.ENTER) {
      if (mpp == false){
        mpp = true;
      } else {
        mpp = false;
      }
    } 
  }
};

let p5sketch1 = new p5(sketch);
