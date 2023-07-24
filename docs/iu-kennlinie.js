let img;
let paint = false;
let mpp = false;

function preload() {
  img = loadImage('dist/pictures/iu-kennlinie.png');
}

function setup() {
  let cnv = createCanvas(600, 400);
  cnv.parent('iukenn1');
}

function draw() {
  let myDegrees = map(mouseY, 0, height, 250, 400);
  let v = p5.Vector.fromAngle(radians(myDegrees), 500);
  let vx = v.x;
  let vy = v.y;

  background(255)
  image(img,0,0)
  strokeWeight(3)
  stroke(255,0,0)
  translate(75,350)

  if (mpp == true){
    vx = 400
    vy = -300
    circle(350, -260, 20);
  }

  if (paint == true) {
    line(0,0,vx,vy);
  }
}

function mouseClicked() {
  if (paint == false){
    paint = true;
  } else {
    paint = false;
  }
}

function keyPressed(){
  if (keyCode === ENTER) {
    if (mpp == false){
      mpp = true;
    } else {
      mpp = false;
    }
  } 
}
