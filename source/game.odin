package game

import rl "vendor:raylib"
import "core:log"
import "core:fmt"
import "core:c"

run: bool
texture: rl.Texture
texture2: rl.Texture
texture2_rot: f32

init :: proc() {
	run = true
	rl.SetConfigFlags({.WINDOW_RESIZABLE, .VSYNC_HINT})
	rl.InitWindow(1280, 720, "AAARP")
	rl.GuiSetStyle(rl.GuiControl.DEFAULT, i32(rl.GuiDefaultProperty.TEXT_SIZE), 30)


	// Anything in `assets` folder is available to load.
	texture = rl.LoadTexture("assets/round_cat.png")

	// A different way of loading a texture: using `read_entire_file` that works
	// both on desktop and web. Note: You can import `core:os` and use
	// `os.read_entire_file`. But that won't work on web. Emscripten has a way
	// to bundle files into the build, and we access those using this
	// special `read_entire_file`.
	if long_cat_data, long_cat_ok := read_entire_file("assets/long_cat.png", context.temp_allocator); long_cat_ok {
		long_cat_img := rl.LoadImageFromMemory(".png", raw_data(long_cat_data), c.int(len(long_cat_data)))
		texture2 = rl.LoadTextureFromImage(long_cat_img)
		rl.UnloadImage(long_cat_img)
	}
}

update :: proc() {
	rl.BeginDrawing()
	rl.ClearBackground({0, 120, 153, 255})
	{
		texture2_rot += rl.GetFrameTime()*50
		source_rect := rl.Rectangle {
			0, 0,
			f32(texture2.width), f32(texture2.height),
		}
		dest_rect := rl.Rectangle {
			300, 220,
			f32(texture2.width)*5, f32(texture2.height)*5,
		}
		rl.DrawTexturePro(texture2, source_rect, dest_rect, {dest_rect.width/2, dest_rect.height/2}, texture2_rot, rl.WHITE)
	}
	rl.DrawTextureEx(texture, rl.GetMousePosition(), 0, 5, rl.WHITE)
	rl.DrawRectangleRec({0, 0, 420, 230}, rl.BLACK)
	rl.GuiLabel({10, 20, 200, 20}, "raygui works!")

	if rl.GuiButton({10, 50, 400, 40}, "Print to log (see console)") {
		log.info("log.info works!")
		fmt.println("fmt.println too.")
	}

	if rl.GuiButton({10, 100, 400, 40}, "Source code (opens GitHub)") {
		rl.OpenURL("https://github.com/karl-zylinski/odin-raylib-web")
	}

	if rl.GuiButton({10, 150, 400, 40}, "Quit") {
		run = false
	}

	rl.EndDrawing()

	// Anything allocated using temp allocator is invalid after this.
	free_all(context.temp_allocator)
}

// In a web build, this is called when browser changes size. Remove the
// `rl.SetWindowSize` call if you don't want a resizable game.
parent_window_size_changed :: proc(w, h: int) {
	rl.SetWindowSize(c.int(w), c.int(h))
}


midi_note_on :: proc(note, vel: int) {
	log.debug("NOTE:", note, vel)
}

midi_note_off :: proc(note, vel: int) {
	log.debug("NOTE OFF:", note, vel)
}


shutdown :: proc() {
	rl.CloseWindow()
}

should_run :: proc() -> bool {
	when ODIN_OS != .JS {
		// Never run this proc in browser. It contains a 16 ms sleep on web!
		if rl.WindowShouldClose() {
			run = false
		}
	}

	return run
}