vim9script

# Constant/Variable declarations {{{1
const NOTEPLUG_FOLDER = expand('<sfile>:h:h')
var win_id: number
 

# Exit(job: job, exit_status: number) {{{1
# This function will handle closing the pop up and managing any tasks that
# were passed through.
def Exit(job: job, exit_status: number)
    popup_close(win_id)
enddef
 

# ProductivityTuiOpenFunc() {{{1
# This function will handle opening the TUI pop up window and any vim level
# formatting involved.
def ProductivityTuiOpenFunc()
    var buf = term_start([&shell, '-ci', 'python ' .. NOTEPLUG_FOLDER .. '/kanban/kanban_main.py'],
                         \ {hidden: 1, term_finish: 'close', exit_cb: 'Exit'})
    
    win_id = popup_create(buf, {line: 5, col: 10, border: [], borderhighlight: ["Normal"],
                                    \ minwidth: 220, minheight: 55})
enddef


# Commands and mappings {{{1
command ProductivityTuiOpen call ProductivityTuiOpenFunc()
nnoremap <leader>npp :ProductivityTuiOpen<CR>
