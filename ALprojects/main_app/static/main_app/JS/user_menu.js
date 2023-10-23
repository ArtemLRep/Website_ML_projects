function clear_period(){
        const period_left = document.getElementById('left_date')
        const period_right = document.getElementById('right_date')
        period_left.value=""
        period_right.value=""
}

function hide_period(){
    const period = document.getElementById('period')
    const period_left_div = document.getElementById('left_date_div')
    const period_right_div = document.getElementById('right_date_div')

    period_left_div.style.display = 'none'
    period_right_div.style.display = 'none'
}

function show_period(){
    const period = document.getElementById('period')
    const period_left_div = document.getElementById('left_date_div')
    const period_right_div = document.getElementById('right_date_div')
    period_left_div.style.display = 'block'
    period_right_div.style.display = 'block'
}

function frozen_period(){
    const period_left = document.getElementById('left_date')
    const period_right = document.getElementById('right_date')
    period_left.setAttribute("readonly","")
    period_right.setAttribute("readonly","")
}
function unfrozen_period(){
    const period_left = document.getElementById('left_date')
    const period_right = document.getElementById('right_date')
    period_left.removeAttribute("readonly")
    period_right.removeAttribute("readonly")
}

function date_to_format(curr_date){
    let day = curr_date.getDate()
    let month = curr_date.getMonth() + 1
    let year = curr_date.getFullYear()
    if (month < 10){
     month = `0${month}`
    }
    if (day < 10){
     day = `0${day}`
    }
    let date_format = year + "-" + month + "-" + day
    return date_format
}
hide_period()
period.addEventListener('change', function() {
        const today = new Date()
        const period_left = document.getElementById('left_date')
        const period_right = document.getElementById('right_date')
        period_right.value = date_to_format(today)

        const period_val = period.value
        if (period_val == 'Month'){
            show_period()
            frozen_period()
            month_before = new Date()
            month_before.setMonth(today.getMonth() - 1)
            period_left.value = date_to_format(month_before)
        }
         else if (period_val == 'Year'){
            show_period()
            frozen_period()
            year_before = new Date()
            year_before.setFullYear(today.getFullYear() - 1)
            period_left.value = date_to_format(year_before)
        }
        else if (period_val == 'Today'){
            clear_period()
            hide_period()
        }
        else {
            show_period()
            unfrozen_period()
        }
    }
)
