var $container;
var filters = {};

function initListView(sortBy) {
  $container = $('.list-container');
  $container.isotope({
    itemSelector: '.list-item',
    getSortData: {
      name: '.sort-name',
      rank: '[data-sort-rank] parseInt',
      level: '[data-sort-level]',
      duration: '.sort-duration'
    },
    sortBy: sortBy
  });

  $container.on('arrangeComplete', function(e, filteredItems) {
    $('.list-count').text(filteredItems.length);
    if (filteredItems.length == 0) {
      $('.no-results').fadeIn(200);
    } else {
      $('.no-results').hide();
    }
  });

  $('.clear-filters').on('click', function(e) {
    e.preventDefault();
    clearFilters();
  })

  $('.sort-link').on('click', function(e) {
    $link = $(e.target);
    var isActive = $link.hasClass('active');
    var isDesc = isActive && $link.hasClass('desc');
    var newClass; 
    
    if (!isActive || isDesc) {
      newClass = 'active';
    } else {
      newClass = 'active desc';
    }
    
    $('.sort-links').find('a').removeClass('active desc');
    $link.addClass(newClass);
    
    $container.isotope({
      sortBy: $link.data('sort-by'),
      sortAscending: !isActive || isDesc
    });
  });

  $('.list-filters').on('change', function(e) {
    var $checkbox = $(e.target);
    manageCheckbox($checkbox);
    var comboFilter = getComboFilter(filters);
    $('.no-results').hide();
    $container.isotope({filter: comboFilter});
  });
}

function clearFilters() {
  $('.list-filters').find('input[type=checkbox]').prop('checked', false);
  filters = {};
  $('.list-filters').trigger('change');
}

function getComboFilter(filters) {
  var i = 0;
  var comboFilters = [];

  for (var prop in filters) {
    var filterGroup = filters[prop];
    // skip to next filter group if it doesn't have any values
    if (!filterGroup.length) {
      continue;
    }
    if (i === 0) {
      // copy to new array
      comboFilters = filterGroup.slice(0);
    } else {
      var filterSelectors = [];
      // copy to fresh array
      var groupCombo = comboFilters.slice(0); // [ A, B ]
      // merge filter Groups
      for (var k = 0, len3 = filterGroup.length; k < len3; k++) {
        for (var j = 0, len2 = groupCombo.length; j < len2; j++) {
          filterSelectors.push(groupCombo[j] + filterGroup[k]); // [ 1, 2 ]
        }

      }
      // apply filter selectors to combo filters for next group
      comboFilters = filterSelectors;
    }
    i++;
  }

  var comboFilter = comboFilters.join(', ');
  return comboFilter;
}

function manageCheckbox($checkbox) {
  var checkbox = $checkbox[0];

  var group = $checkbox.parents('.list-checkbox-group').attr('data-group');
  // create array for filter group, if not there yet
  var filterGroup = filters[group];
  if (!filterGroup) {
    filterGroup = filters[group] = [];
  }

  var isAll = $checkbox.hasClass('all');
  // reset filter group if the all box was checked
  if (isAll) {
    delete filters[group];
    if (!checkbox.checked) {
      checkbox.checked = 'checked';
    }
  }
  
  // index of
  var index = $.inArray(checkbox.value, filterGroup);

  if (checkbox.checked) {
    var selector = isAll ? 'input' : 'input.all';
    $checkbox.siblings(selector).removeAttr('checked');


    if (!isAll && index === -1) {
      // add filter to group
      filters[group].push(checkbox.value);
    }

  } else if (!isAll) {
    // remove filter from group
    filters[group].splice(index, 1);
    // if unchecked the last box, check the all
    if (!$checkbox.siblings('[checked]').length) {
      $checkbox.siblings('input.all').attr('checked', 'checked');
    }
  }
}